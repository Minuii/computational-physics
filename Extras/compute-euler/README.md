# Compute e to N Decimals

Calculates Euler's number by summing the series `e = sum(1/k!)`, using Python's `decimal` module.

## Run
```bash
python eulergen.py
```
Enter the number of decimal places when prompted.

## How it works
Precision is set to `n + 100` digits and `n + 100` terms are summed as a safety margin, then the result is rounded to `n` decimals with `quantize`. The series converges very fast, so this is accurate for large `n`, though it is more terms than strictly needed.
