# Compute Pi to N Decimals

Calculates pi with the Chudnovsky series, using Python's `decimal` module for arbitrary precision.

## Run
```bash
python pigen.py
```
Enter the number of decimal places when prompted.

## How it works
Sums `n` terms of the Chudnovsky series, scales by `12 / 640320^1.5`, then takes the reciprocal. Each term adds roughly 14 correct digits.

## Limitations
- The working precision is fixed at 1000 digits (`getcontext().prec = 1000`), so asking for more than about 1000 decimals gives wrong output unless you raise it.
- The number of series terms is set to `n`, which is far more than needed. `n / 14` terms would be enough, so large `n` runs slower than necessary.
