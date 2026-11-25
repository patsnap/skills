(async function callPulse(tools, options) {
  const quote = value => "'" + String(value).replaceAll("'", "'\\''") + "'";
  if (['get_mcp_brief_info', 'get_mcp_brief_data'].includes(options.tool)) {
    const connection = options.connection ? ['--connection', options.connection]
      : ['--codex-config', ...(options.codexConfig ? [options.codexConfig] : [])];
    const command = [options.python, options.skill + '/scripts/call_mcp.py', ...connection,
      '--server', 'eureka-pulse', '--workspace', options.workspace, '--tool', options.tool, '--arguments', options.arguments];
    const result = await tools.exec_command({cmd: command.map(quote).join(' '), max_output_tokens: 2000, yield_time_ms: 1000});
    let current = result;
    const chunks = [current.output];
    while (current.session_id) {
      current = await tools.write_stdin({session_id: current.session_id, chars: '', max_output_tokens: 2000, yield_time_ms: 1000});
      chunks.push(current.output);
    }
    if (current.exit_code !== 0) throw new Error('详情读取失败：' + chunks.join(''));
    return JSON.parse(chunks.join(''));
  }
  const qualified = 'mcp__eureka_pulse__' + options.tool;
  if (typeof tools[qualified] !== 'function') throw new Error('当前宿主未提供目标 Tool');
  const run = async arguments_ => {
    const result = await tools.exec_command({cmd: [options.python, options.skill + '/scripts/monitor.py', ...arguments_].map(quote).join(' '), max_output_tokens: 10000});
    if (result.exit_code !== 0) throw new Error('执行失败：' + result.output);
    if (result.original_token_count > 10000) throw new Error('文件交接程序输出不完整');
    return JSON.parse(result.output);
  };
  const call = await run(['prepare-call', '--workspace', options.workspace, '--tool', options.tool, '--arguments', options.arguments]);
  let offset = 0;
  const chunks = [];
  while (true) {
    const part = await run(['read-chunk', '--input', call.arguments, '--offset', String(offset)]);
    chunks.push(part.text);
    if (part.complete) break;
    if (part.next_offset <= offset) throw new Error('参数文件读取未继续前进');
    offset = part.next_offset;
  }
  const response = await tools[qualified](JSON.parse(chunks.join('')));
  const source = JSON.stringify(response);
  for (let index = 0; index < source.length;) {
    let end = Math.min(index + 6000, source.length);
    const last = source.charCodeAt(end - 1);
    if (end < source.length && last >= 0xD800 && last <= 0xDBFF) end -= 1;
    const method = index === 0 ? 'writeFile' : 'appendFile';
    const options_ = index === 0 ? ',{flag:"wx"}' : '';
    const result = await tools.mcp__node_repl__js({code: "var pulseBridgeFs = await import('node:fs/promises'); await pulseBridgeFs." + method + '(' + JSON.stringify(call.response) + ',' + JSON.stringify(source.slice(index, end)) + options_ + ');', title: '保存 MCP 原始响应'});
    if (result.isError) throw new Error('MCP 原始响应保存失败');
    index = end;
  }
  return await run(['finish-call', '--workspace', options.workspace, '--call-dir', call.call_dir]);
})
