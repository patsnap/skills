(() => {
  'use strict';
  const chartTheme = getComputedStyle(document.documentElement);
  const chartColor = name => {
    const value = chartTheme.getPropertyValue(name).trim();
    if (!value) throw new Error('图表主题缺少颜色：' + name);
    return value;
  };
  const colors = Array.from({ length: 10 }, (_, index) => chartColor('--color-chart-' + (index + 1)));
  const typeNames = { patent: '专利', paper: '论文', news: '新闻' };
  const instances = [];
  const receipts = [];
  const summaryMetrics = [];
  const create = (tag, className, text) => {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  };
  const assert = (condition, message) => { if (!condition) throw new Error(message); };
  const categories = dimension => Object.entries(dimension.members)
    .map(([name, keys]) => ({ name, keys, value: keys.length }))
    .filter(item => item.value > 0).sort((a, b) => b.value - a.value || a.name.localeCompare(b.name));

  function showRecords(host, period, keys, title) {
    host.replaceChildren();
    host.hidden = false;
    document.getElementById('metric-source-title').textContent = title + ' · ' + keys.length + ' 条';
    host.append(create('p', 'history-note', period.target.start_date + ' 至 ' + period.target.end_date));
    const list = create('ol');
    for (const key of keys) {
      const record = period.records[key];
      assert(record, '统计记录未在原始资料索引中找到');
      const item = create('li', 'source-record');
      item.dataset.historyRecord = key;
      if (record.anchor) {
        assert(document.getElementById(record.anchor), '资料位置未在报告中找到');
        const link = create('a', 'source-record-title', record.title);
        link.href = '#' + record.anchor;
        link.addEventListener('click', () => metricDialog.close());
        item.append(link);
      } else if (record.link) {
        const url = new URL(record.link);
        assert(['https:', 'http:'].includes(url.protocol), '资料链接协议不受支持');
        const link = create('a', 'source-record-title', record.title);
        link.href = record.link;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        item.append(link);
      } else item.append(create('span', 'source-record-title', record.title));
      if (record.source_periods?.length) {
        item.dataset.sourcePeriods = JSON.stringify(record.source_periods.map(source => source.period));
        item.append(create('p', 'source-record-periods', '来源期次：' + record.source_periods.map(source =>
          source.period_type === 'month' ? source.start_date.slice(0, 7) : source.start_date).join('、')));
      }
      const field = record.technical_title?.trim() ? 'technical_title' : 'abstract';
      const text = record[field]?.trim();
      if (text) {
        const summary = create('p', 'source-record-summary', text);
        summary.dataset.sourceField = field;
        item.append(summary);
      }
      list.append(item);
    }
    host.append(list);
    if (!keys.length) host.append(create('p', '', '该期完整结果中没有符合本项条件的记录。'));
  }

  const metricDialog = document.getElementById('metric-source-dialog');
  const metricBody = document.getElementById('metric-source-body');
  let metricTrigger = null;
  document.getElementById('metric-source-close').addEventListener('click', () => metricDialog.close());
  metricDialog.addEventListener('click', event => {
    const bounds = metricDialog.getBoundingClientRect();
    if (event.target === metricDialog && (event.clientX < bounds.left || event.clientX > bounds.right ||
        event.clientY < bounds.top || event.clientY > bounds.bottom)) metricDialog.close();
  });
  metricDialog.addEventListener('close', () => {
    if (metricTrigger) metricTrigger.focus({ preventScroll: true });
  });

  function openSourceList(period, keys, title, trigger, drawer = false) {
    metricTrigger = trigger;
    metricDialog.classList.toggle('chart-source-drawer', drawer);
    showRecords(metricBody, period, keys, title);
    if (!metricDialog.open) metricDialog.showModal();
    metricBody.scrollTop = 0;
    document.getElementById('metric-source-close').focus({ preventScroll: true });
  }

  function bindMetric(button, period, keys, title) {
    button.setAttribute('aria-controls', metricDialog.id);
    button.setAttribute('aria-haspopup', 'dialog');
    button.addEventListener('click', () => {
      openSourceList(period, keys, title, button);
    });
  }

  function showMetricGroups(period, metric, focusIndex = null) {
    metricBody.replaceChildren();
    metricBody.hidden = false;
    metricBody.scrollTop = 0;
    document.getElementById('metric-source-title').textContent = metric.label + ' · ' + metric.value + ' 项';
    metricBody.append(create('p', 'history-note', period.target.start_date + ' 至 ' + period.target.end_date));
    const coverage = metric.coverage;
    if (coverage) metricBody.append(create('p', 'history-note', '有信息 ' + coverage.classified + '／' + coverage.eligible +
      ' 条' + coverage.population + '；同一资料可属于多个项目。'));
    const list = create('ol');
    metric.groups.forEach((group, index) => {
      const item = create('li', 'source-record source-group');
      const button = create('button', 'source-record-title metric-group-open', group.label);
      button.type = 'button';
      button.dataset.groupIndex = index;
      button.dataset.recordKeys = JSON.stringify(group.keys);
      button.setAttribute('aria-label', group.label + '，' + group.keys.length + ' 条资料，查看来源');
      button.addEventListener('click', () => {
        showRecords(metricBody, period, group.keys, metric.label + ' · ' + group.label);
        const back = create('button', 'metric-group-back', '返回' + metric.label);
        back.type = 'button';
        back.addEventListener('click', () => showMetricGroups(period, metric, index));
        metricBody.prepend(back);
        metricBody.scrollTop = 0;
        back.focus({ preventScroll: true });
      });
      item.append(button, create('p', 'source-record-periods', group.keys.length + ' 条资料'));
      list.append(item);
    });
    metricBody.append(list);
    if (focusIndex !== null) metricBody.querySelectorAll('.metric-group-open')[focusIndex].focus({ preventScroll: true });
  }

  const overview = document.getElementById('metric-overview');
  const reportRecords = {};
  for (const record of document.querySelectorAll('article.record[data-record-key]')) {
    if (!reportRecords[record.dataset.recordKey]) {
      reportRecords[record.dataset.recordKey] = { title: record.querySelector('.record-title').textContent, anchor: record.id };
    }
  }
  const reportPeriod = { target: { start_date: overview.dataset.startDate, end_date: overview.dataset.endDate }, records: reportRecords };
  for (const button of overview.querySelectorAll('[data-summary-metric]')) {
    const keys = JSON.parse(button.dataset.recordKeys);
    const metric = button.dataset.metric ? JSON.parse(button.dataset.metric) :
      { key: button.dataset.summaryMetric, value: Number(button.dataset.value), kind: 'records', keys };
    assert(keys.length === new Set(keys).size && keys.length === metric.keys.length && metric.keys.every(key => keys.includes(key)),
      '概览卡片资料索引不一致');
    assert(keys.every(key => reportRecords[key]), '概览卡片引用了未显示的资料');
    const label = button.querySelector('.visual-metric-name').textContent;
    assert(metric.value === Number(button.dataset.value), '概览卡片数量与展示数据不一致');
    if (metric.kind === 'groups') {
      assert(metric.value === metric.groups.length && new Set(metric.groups.map(group => group.label)).size === metric.value,
        '概览卡片项目数量不一致');
      const groupedKeys = new Set(metric.groups.flatMap(group => group.keys));
      assert(groupedKeys.size === keys.length && keys.every(key => groupedKeys.has(key)), '概览分类卡片的来源范围不一致');
      assert(metric.coverage.classified === keys.length && keys.length <= metric.coverage.eligible, '概览卡片分类覆盖数量无效');
      button.setAttribute('aria-controls', metricDialog.id);
      button.setAttribute('aria-haspopup', 'dialog');
      button.addEventListener('click', () => {
        metricTrigger = button;
        metricDialog.classList.remove('chart-source-drawer');
        showMetricGroups(reportPeriod, metric);
        if (!metricDialog.open) metricDialog.showModal();
        document.getElementById('metric-source-close').focus({ preventScroll: true });
      });
    } else {
      assert(metric.kind === 'records' && metric.value === keys.length, '概览资料卡片数量与去重资料不一致');
      bindMetric(button, reportPeriod, keys, label);
    }
    summaryMetrics.push({ ...metric, label });
  }

  function baseOption(host) {
    return {
      animation: false,
      color: colors,
      textStyle: { fontFamily: getComputedStyle(host).fontFamily, fontSize: 14, color: chartColor('--color-text-secondary') },
      aria: { enabled: true },
      tooltip: { trigger: 'item', renderMode: 'html', enterable: false, confine: true },
      grid: { left: 12, right: 48, top: 36, bottom: 32, containLabel: true },
      xAxis: { type: 'value', minInterval: 1, axisLabel: { color: chartColor('--color-text-tertiary'), fontSize: 12 },
        splitLine: { lineStyle: { color: chartColor('--color-border-default'), type: 'dashed' } } },
      yAxis: { type: 'category', axisLabel: { color: chartColor('--color-text-secondary'), fontSize: 12, width: 220, overflow: 'break' },
        axisLine: { lineStyle: { color: chartColor('--color-border-default') } }, axisTick: { show: false } }
    };
  }

  function draw(panel, type, option, resolvePoint) {
    assert(typeof echarts !== 'undefined', '图表资源未加载');
    const scroll = create('div', 'visual-chart-scroll');
    const host = create('div', 'visual-chart');
    host.style.height = Math.max(320, (option.yAxis?.data?.length || 0) * 44 + 100) + 'px';
    host.setAttribute('role', 'img');
    host.setAttribute('aria-label', panel.querySelector('h3').textContent);
    host.tabIndex = 0;
    scroll.append(host);
    panel.append(scroll);
    const chart = echarts.init(host, null, { renderer: 'svg' });
    chart.setOption({ ...baseOption(host), ...option });
    chart.on('click', parameters => {
      if (parameters.componentType === 'series') {
        chart.dispatchAction({ type: 'hideTip' });
        resolvePoint(parameters);
      }
    });
    const observer = new ResizeObserver(() => chart.resize());
    observer.observe(host);
    instances.push(chart);
    panel.dataset.presentation = type;
    return chart;
  }

  function panelFrame(root, title, note, id, period) {
    const panel = create('article', 'visual-panel');
    panel.dataset.dimension = id;
    panel.append(create('h3', '', title), create('p', 'history-note', note));
    root.querySelector('.visual-panels').append(panel);
    return { panel, open: (keys, label, source = period) =>
      openSourceList(source, keys, title + ' · ' + label, panel.querySelector('.visual-chart'), true) };
  }

  function distribution(root, period, dimension) {
    const values = categories(dimension);
    if (!values.length) return false;
    const note = period.target.start_date + ' 至 ' + period.target.end_date + ' · ' + dimension.population +
      '；有分类或公司信息 ' + dimension.classified_count + '／' + dimension.eligible_count + ' 条。多值资料分别计入对应项目。';
    const excluded = Object.entries(dimension.components || {}).filter(([, item]) => !item.complete).map(([kind]) => typeNames[kind]);
    const unknown = excluded.length ? '部分期次的评分或资料集合不完整，未纳入对应期次的' + excluded.join('、') + '。' : '';
    let presentation;
    const selection = JSON.parse(root.querySelector('.intelligence-visual-data').textContent).dimension_selection;
    const productLine = dimension.field_key === 'product_line' || selection?.candidates?.some(
      item => item.field_key === dimension.field_key && item.role === 'product_line');
    if (values.length <= 3 && !productLine) {
      const frame = panelFrame(root, dimension.name, note + unknown, dimension.id, period);
      const cards = create('div', 'visual-distribution-cards');
      frame.panel.append(cards);
      for (const item of values) {
        const button = create('button', 'visual-metric');
        button.type = 'button';
        button.dataset.dimension = dimension.id;
        button.dataset.value = item.value;
        button.dataset.recordKeys = JSON.stringify(item.keys);
        button.title = dimension.name + ' · ' + item.name + ' · ' + note + unknown;
        button.setAttribute('aria-label', dimension.name + '，' + item.name + '，' + item.value + ' 条资料，查看来源');
        button.append(create('strong', '', String(item.value)), create('span', 'visual-metric-name', item.name));
        bindMetric(button, period, item.keys, dimension.name + ' · ' + item.name);
        cards.append(button);
      }
      presentation = 'cards';
      frame.panel.dataset.presentation = presentation;
    } else {
      const frame = panelFrame(root, dimension.name, note + unknown, dimension.id, period);
      const points = [...values].reverse();
      draw(frame.panel, 'bar', {
        yAxis: { ...baseOption(frame.panel).yAxis, data: points.map(item => item.name) },
        series: [{ type: 'bar', barMaxWidth: 28, data: points.map(item => item.value),
          label: { show: true, position: 'right', color: chartColor('--color-text-secondary') } }]
      }, parameters => frame.open(points[parameters.dataIndex].keys, points[parameters.dataIndex].name));
      presentation = frame.panel.dataset.presentation;
    }
    receipts.push({ dimension: dimension.id, period: period.target.period, presentation,
      scope: period.scope || 'period', range: period.scope === 'range' ? period.target : undefined,
      categories: values.length, points: values.map(item => ({ name: item.name, value: item.value, keys: item.keys })) });
    return true;
  }

  function rangeDistribution(root, model, dimension) {
    const eligible = new Set(), members = new Map(), records = {}, components = {};
    for (const period of model.periods) {
      if (period.status !== 'available') continue;
      const types = Object.fromEntries(Object.entries(period.members).filter(([, keys]) => keys?.length)
        .map(([kind, keys]) => [typeNames[kind], keys]));
      const typeKeys = Object.values(types).flat();
      const value = dimension.id === 'record-types' ? { ...dimension, members: types,
        eligible_members: typeKeys, eligible_count: typeKeys.length } : period.dimensions.find(item => item.id === dimension.id);
      if (!value) continue;
      assert(value.signature === dimension.signature, '统计范围内的分类定义不同，无法合并资料分布');
      assert(value.eligible_members.length === value.eligible_count, '范围统计缺少完整适用资料索引');
      value.eligible_members.forEach(key => eligible.add(key));
      for (const [kind, component] of Object.entries(value.components || {})) {
        components[kind] = { complete: (components[kind]?.complete ?? true) && component.complete };
      }
      for (const [label, keys] of Object.entries(value.members)) {
        if (!members.has(label)) members.set(label, new Set());
        for (const key of keys) {
          members.get(label).add(key);
          const sources = records[key]?.source_periods || [];
          records[key] = { ...period.records[key], source_periods: sources.some(source => source.period === period.target.period)
            ? sources : [...sources, period.target] };
        }
      }
    }
    const values = Object.fromEntries([...members].map(([label, keys]) => [label, [...keys]]));
    const aggregate = { ...dimension, members: values, components,
      population: '统计范围内已取得的有效资料，跨期按稳定身份去重', eligible_count: eligible.size,
      classified_count: new Set(Object.values(values).flat()).size };
    const target = { ...model.target, start_date: model.periods[0].target.start_date, end_date: model.periods.at(-1).target.end_date };
    return distribution(root, { target, records, scope: 'range' }, aggregate);
  }

  function companyRouteBubble(root, model, dimension) {
    const groups = new Map();
    const eligible = new Set();
    const included = [];
    for (const period of model.periods) {
      if (period.status !== 'available') continue;
      const routes = period.dimensions.find(item => item.id === dimension.id);
      const companies = period.dimensions.find(item => item.id === 'company:patent');
      if (!routes?.components?.patent?.complete) continue;
      assert(routes.signature === dimension.signature, '统计范围内的方向字段定义不同，无法合并公司与技术方向资料');
      const component = routes.components.patent;
      assert(component.eligible_members.length === component.eligible_count, '交叉统计缺少完整适用资料索引');
      component.eligible_members.forEach(key => eligible.add(key));
      included.push(period.target.period);
      for (const [company, companyKeys] of Object.entries(companies?.members || {})) {
        const keys = new Set(companyKeys);
        for (const [route, routeKeys] of Object.entries(component.members)) {
          const members = routeKeys.filter(key => keys.has(key));
          if (!members.length) continue;
          if (!groups.has(company)) groups.set(company, new Map());
          const companyGroups = groups.get(company);
          if (!companyGroups.has(route)) companyGroups.set(route, new Map());
          const records = companyGroups.get(route);
          for (const key of members) {
            const previous = records.get(key);
            records.set(key, { ...period.records[key],
              source_periods: [...(previous?.source_periods || []), period.target] });
          }
        }
      }
    }
    const points = [...groups].flatMap(([company, routes]) => [...routes].map(([route, records]) =>
      ({ company, route, records: Object.fromEntries(records), keys: [...records.keys()], value: records.size })));
    if (!points.length) return false;
    const routes = [...new Set(points.map(point => point.route))].sort();
    const companies = [...new Set(points.map(point => point.company))].sort();
    const maximum = Math.max(...points.map(point => point.value));
    const target = { start_date: model.periods[0].target.start_date, end_date: model.periods.at(-1).target.end_date };
    const classified = new Set(points.flatMap(point => point.keys)).size;
    const note = '统计范围：' + target.start_date + ' 至 ' + target.end_date + ' · 汇总已取得的 ' + included.length +
      ' 期完整资料，有申请人与分类的高相关专利 ' + classified + '／' + eligible.size +
      ' 条。跨期相同资料按稳定身份去重；气泡面积表示数量，多申请人或多分类资料分别计入对应项目。';
    const crossDimension = 'company-route:' + dimension.field_key;
    const frame = panelFrame(root, '公司 × ' + dimension.name, note, crossDimension, { target, records: {} });
    frame.panel.dataset.chartRole = 'company-cross';
    const receipt = { dimension: crossDimension, source_dimension: dimension.id, presentation: 'bubble', company_dimension: 'company:patent',
      field_key: dimension.field_key, scope: 'range', range: target, periods: included,
      classified_count: classified, eligible_count: eligible.size, continuous_basis_confirmed: false,
      points: points.map(point => ({ company: point.company, route: point.route, value: point.value, keys: point.keys,
        source_periods: Object.fromEntries(point.keys.map(key => [key, point.records[key].source_periods.map(source => source.period)])) })) };
    draw(frame.panel, 'bubble', {
      grid: { left: 16, right: 56, top: 36, bottom: 96, containLabel: true },
      tooltip: { trigger: 'item', confine: true, formatter: parameters => {
        const point = points[parameters.value[3]];
        const text = create('div');
        text.append(create('strong', '', point.company), create('div', '', point.route + ' · ' + point.value + ' 条高相关专利'),
          create('div', '', target.start_date + ' 至 ' + target.end_date));
        return text;
      } },
      xAxis: { type: 'category', data: routes, axisLabel: { color: chartColor('--color-text-tertiary'), fontSize: 12, interval: 0, rotate: 25 },
        splitLine: { show: true, lineStyle: { color: chartColor('--color-border-default'), type: 'dashed' } } },
      yAxis: { ...baseOption(frame.panel).yAxis, data: companies,
        splitLine: { show: true, lineStyle: { color: chartColor('--color-border-default'), type: 'dashed' } } },
      series: [{ type: 'scatter', symbolSize: value => 40 * Math.sqrt(value[2] / maximum),
        itemStyle: { color: colors[0], opacity: 0.75 }, emphasis: { scale: 1.15 },
        labelLayout: { hideOverlap: true },
        label: { show: true, position: 'top', distance: 4, formatter: parameters => String(parameters.value[2]), color: chartColor('--color-text-secondary'), fontSize: 12 },
        data: points.map((point, index) => [routes.indexOf(point.route), companies.indexOf(point.company), point.value, index]) }]
    }, parameters => {
      const point = points[parameters.value[3]];
      frame.open(point.keys, point.company + ' · ' + point.route, { target, records: point.records });
    });
    receipts.push(receipt);
    return true;
  }

  function historicalEntries(model, dimension) {
    const entries = model.periods.map(period => ({ period, dimension: period.status === 'available'
      ? period.dimensions.find(item => item.id === dimension.id && item.signature === dimension.signature) : null }));
    const defined = entries.filter(entry => entry.dimension);
    const kinds = dimension.components ? Object.keys(dimension.components).filter(kind =>
      defined.every(entry => entry.dimension.components[kind].complete)) : [];
    const omitted = dimension.components ? Object.keys(dimension.components).filter(kind => !kinds.includes(kind)) : [];
    for (const entry of entries) {
      if (!entry.dimension) {
        entry.reason = entry.period.status === 'available' ? '字段缺失或定义不同' : entry.period.status;
        continue;
      }
      if (entry.dimension.components) {
        const parts = kinds.map(kind => entry.dimension.components[kind]);
        const members = {};
        for (const part of parts) {
          for (const [label, keys] of Object.entries(part.members)) (members[label] ||= []).push(...keys);
        }
        entry.dimension = { ...entry.dimension, members,
          classified_count: parts.reduce((sum, part) => sum + part.classified_count, 0),
          eligible_count: parts.reduce((sum, part) => sum + part.eligible_count, 0) };
        if (!parts.length) {
          entry.reason = '没有共同的评分完整资料类型';
          entry.dimension = null;
          continue;
        }
      }
      if (entry.dimension.eligible_count > 0 && entry.dimension.classified_count === 0) {
        entry.reason = '没有实际分类值';
        entry.dimension = null;
      }
    }
    return { entries, kinds, omitted };
  }

  function historicalDimension(root, model, dimension) {
    const { entries, kinds, omitted } = historicalEntries(model, dimension);
    const valid = entries.filter(entry => entry.dimension);
    if (valid.length < 2) return false;
    const first = entries.indexOf(valid[0]), last = entries.indexOf(valid.at(-1));
    const window = entries.slice(first, last + 1);
    const matching = window.map(entry => entry.dimension ? entry : null);
    const labels = [...new Set(valid.flatMap(entry => Object.keys(entry.dimension.members)))].sort();
    if (!labels.length) return false;
    const anchor = valid.find(entry => entry.period.target.period === model.target.period)?.period || valid.at(-1).period;
    const version = valid[0].period.comparison_basis.config_version;
    const continuous = version !== undefined && valid.every(entry => entry.period.comparison_basis.config_version === version);
    const points = [];
    const keysFor = (entry, label) => entry.dimension.members[label] ||
      (entry.dimension.classified_count === entry.dimension.eligible_count ? [] : null);
    labels.forEach(label => matching.forEach(entry => {
      if (!entry) return;
      const keys = keysFor(entry, label);
      if (keys === null) return;
      const point = { name: entry.period.target.period + ' · ' + label, value: keys.length, keys, period: entry.period };
      points.push(point);
    }));
    const coverage = valid.map(entry => ({ period: entry.period.target.period,
      classified: entry.dimension.classified_count, eligible: entry.dimension.eligible_count }));
    const population = kinds.length ? kinds.map(kind => typeNames[kind]).join('、') + '中的高相关技术资料' : dimension.population;
    const coverageNote = coverage.map(item => item.period + '：' + item.classified + '／' + item.eligible).join('；');
    const frame = panelFrame(root, dimension.name + ' · 历史变化',
      population + '。各期有分类或公司信息／适用资料：' + coverageNote + '。缺失位置保持空缺，多值资料分别计数。' +
      (omitted.length ? '评分或资料集合不完整的类型未纳入共同比较：' + omitted.map(kind => typeNames[kind]).join('、') + '。' : ''), dimension.id, anchor);
    const dates = window.map(entry => model.target.period_type === 'month'
      ? entry.period.target.start_date.slice(0, 7) : entry.period.target.start_date);
    const symbols = ['circle', 'rect', 'triangle', 'diamond', 'roundRect', 'pin', 'arrow'];
    draw(frame.panel, 'line', {
      grid: { left: 16, right: 32, top: 64, bottom: 36, containLabel: true },
      tooltip: { trigger: 'axis', confine: true, axisPointer: { type: 'line' } },
      xAxis: { type: 'category', boundaryGap: false, data: dates, axisLabel: { color: chartColor('--color-text-tertiary'), fontSize: 12 } },
      yAxis: { type: 'value', min: 0, minInterval: 1, splitLine: { lineStyle: { color: chartColor('--color-border-default'), type: 'dashed' } } },
      legend: { type: 'scroll', top: 8, left: 12, right: 12, tooltip: { show: true },
        textStyle: { color: chartColor('--color-text-secondary'), fontSize: 12, width: 180, overflow: 'truncate' },
        pageTextStyle: { color: chartColor('--color-text-secondary'), fontSize: 12 } },
      series: labels.map((label, index) => ({ name: label, type: 'line', connectNulls: false, smooth: false,
        showSymbol: true, symbol: symbols[index % symbols.length], symbolSize: 8,
        lineStyle: { width: 2, type: index < colors.length ? 'solid' : 'dashed' },
        emphasis: { focus: 'series' }, labelLayout: { hideOverlap: true },
        label: { show: true, color: chartColor('--color-text-secondary') }, data: matching.map(entry => entry ? keysFor(entry, label)?.length ?? null : null) }))
    }, parameters => {
      const entry = matching[parameters.dataIndex];
      const keys = entry && keysFor(entry, parameters.seriesName);
      assert(keys !== null && keys !== undefined, '历史图表引用了未知数量');
      frame.open(keys, parameters.seriesName, entry.period);
    });
    receipts.push({ dimension: dimension.id, presentation: frame.panel.dataset.presentation, categories: labels.length,
      periods: matching.map(entry => entry ? entry.period.target.period : null), signature: dimension.signature,
      population_kinds: kinds, omitted_kinds: omitted, coverage, continuous_basis_confirmed: continuous,
      excluded_periods: entries.filter(entry => !entry.dimension).map(entry => ({ period: entry.period.target.period, reason: entry.reason })),
      points: points.map(point => ({ name: point.name, value: point.value, keys: point.keys, period: point.period.target.period })) });
    return true;
  }

  for (const root of document.querySelectorAll('.intelligence-visuals')) {
    const receiptStart = receipts.length;
    const model = JSON.parse(root.querySelector('.intelligence-visual-data').textContent);
    assert(model.schema_version === 3, '统计展示数据版本无效');
    const available = model.periods.filter(period => period.status === 'available');
    const current = available.find(period => period.target.period === model.target.period);
    const scope = root.querySelector('.visual-scope');
    const start = model.periods[0].target.start_date;
    const end = model.periods.at(-1).target.end_date;
    scope.append(create('p', 'history-note', start + ' 至 ' + end + ' · ' + available.length + ' 个可统计周期。数量表示监控收录情况。'));
    const chosen = current || available.at(-1);
    if (chosen) {
      if (!current) scope.append(create('p', 'history-note', '目标' + (model.target.period_type === 'month' ? '月' : '周') + '没有完整资料，以下使用 ' + chosen.target.period + ' 期的已有结果；各项均显示对应日期。'));
      const candidates = new Map();
      for (const period of [...available].reverse()) {
        for (const dimension of period.dimensions) {
          if (!candidates.has(dimension.id)) candidates.set(dimension.id, { period, dimension });
        }
      }
      const selection = model.dimension_selection;
      if (selection) {
        const host = root.querySelector('.visual-panels');
        const trends = create('div', 'visual-trend-row');
        host.append(trends);
        for (const [role, id] of [['company-trend', selection.company_trend_dimension],
          ['category-trend', selection.category_trend_dimension]]) {
          if (!id) continue;
          const candidate = candidates.get(id);
          assert(candidate, '已选择的趋势维度没有有效资料');
          const { dimension } = candidate;
          if (!historicalDimension(root, model, dimension)) rangeDistribution(root, model, dimension);
          const panel = [...host.children].find(element => element.classList.contains('visual-panel') && element.dataset.dimension === id);
          if (panel) {
            panel.dataset.chartRole = role;
            if (role === 'company-trend') panel.querySelector('h3').textContent = '公司趋势 · ' + dimension.name;
            trends.append(panel);
          }
        }
        if (!trends.children.length) trends.remove();
        if (selection.company_route_field) {
          const candidate = candidates.get('field:' + selection.company_route_field);
          assert(candidate && companyRouteBubble(root, model, candidate.dimension), '已选择的公司交叉维度没有有效资料');
        }
      } else {
        for (const { dimension } of candidates.values()) {
          if (dimension.field_key === model.company_route_field && companyRouteBubble(root, model, dimension)) continue;
          if (!historicalDimension(root, model, dimension)) {
            if (available.length > 1 && categories(dimension).length) {
              scope.append(create('p', 'history-note', dimension.name + '不足两个同定义且可统计的期次，汇总统计范围内的有效资料。'));
            }
            rangeDistribution(root, model, dimension);
          }
        }
      }
      const historical = receipts.slice(receiptStart).filter(item => item.periods);
      if (historical.some(item => !item.continuous_basis_confirmed)) {
        scope.append(create('p', 'history-note', '图表展示各期已收录资料；无法确认历史检索范围及评分规则是否调整，不计算跨期增长率。'));
      }
      if (receipts.length === receiptStart) {
        rangeDistribution(root, model, { id: 'record-types', name: '资料收录', signature: 'record-types' });
      }
    }
    if (receipts.length === receiptStart) scope.append(create('p', 'history-note', '没有可用于统计展示的有效项目。'));
    const hasHistoryNotes = model.mode === 'history' && available.length > 1;
    if (current && receipts.length > receiptStart && !root.querySelector('.visual-panel') && !hasHistoryNotes) {
      const section = root.closest('section');
      section.hidden = true;
      for (const link of document.querySelectorAll('.chapter-link')) {
        if (link.hash === '#' + section.id) link.closest('.nav-chapter').hidden = true;
      }
    }
    root.dataset.presentationReady = 'true';
    const section = root.closest('section');
    const sectionTitle = section.querySelector('.section-heading h2');
    if (sectionTitle && !receipts.slice(receiptStart).some(item => item.periods)) {
      const title = current ? '本期情报分布' : chosen ? '历史资料分布' : '资料概况';
      sectionTitle.textContent = title;
      for (const link of document.querySelectorAll('.chapter-link')) {
        if (link.hash === '#' + section.id) link.firstChild.textContent = title;
      }
    }
  }
  [...document.querySelectorAll('main > section:not([hidden])')].forEach((section, index) => {
    const number = section.querySelector('.section-number');
    if (number) number.textContent = String(index + 1).padStart(2, '0');
  });
  window.addEventListener('beforeprint', () => { for (const chart of instances) chart.resize(); });
  window.addEventListener('afterprint', () => { for (const chart of instances) chart.resize(); });
  window.EurekaIntelligenceCharts = Object.freeze({ receipts, summaryMetrics });
})();
