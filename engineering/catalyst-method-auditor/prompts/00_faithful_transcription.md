# 截图/扫描件忠实转写要求

当输入为图片、截图或扫描 PDF 时，先执行忠实转写，再调用 `scripts/run_audit.py`。

转写原则：

1. 保留原文顺序，不重新组织为 proposal。
2. 保留所有数字、单位、化学式、样品名、温度、时间、气氛、仪器名。
3. 不补写原文没有的信息。
4. 看不清的内容标记为 `[无法辨认]`，不得猜测。
5. 数字和单位尽量按原文保留，例如 `1.39 g`、`195 °C`、`20% H2/Ar`、`0.5 h`。
6. 输出纯文本或 Markdown 均可，但不得加入审核意见。

转写完成后保存为 `input_transcription.md` 或 `input_transcription.txt`，再执行：

```bash
python scripts/run_audit.py --input input_transcription.md --out outputs
```
