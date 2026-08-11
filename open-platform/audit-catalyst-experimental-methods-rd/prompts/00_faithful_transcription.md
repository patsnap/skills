# Faithful transcription of screenshots and scans

When the input is an image, screenshot, or scanned PDF, transcribe it faithfully before running `scripts/run_audit.py`.

Requirements:

1. Preserve source order; do not reorganize the material into a proposal.
2. Preserve every number, unit, formula, sample name, temperature, duration, atmosphere, and instrument name.
3. Do not add information absent from the source.
4. Mark illegible content as `[illegible]`; never guess.
5. Preserve the original notation where practical, for example `1.39 g`, `195 °C`, `20% H2/Ar`, and `0.5 h`.
6. Plain text or Markdown is acceptable, but do not insert audit opinions.
7. Preserve decimal separators and explicitly flag any ambiguous comma/period usage.
8. Preserve page or image boundaries when they affect sequence or context.

Save the result as `input_transcription.md` or `input_transcription.txt`, then run:

```bash
python scripts/run_audit.py --input input_transcription.md --out outputs
```
