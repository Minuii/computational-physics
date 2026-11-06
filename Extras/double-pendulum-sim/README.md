# Double Pendulum Simulator

Simulates a double pendulum, a classic chaotic system, and animates it in real time.

## Features
- Animated pendulum with a trailing path (left) next to a live plot of both angles over time (right).
- Equations of motion integrated with SciPy's `odeint`.
- Energy tracking to check the integration stays accurate.
- Interactive prompts for rod lengths, masses, initial angles (degrees) and duration. Press Enter to accept the defaults (1 m, 1 kg, 120 and 30 degrees, 20 s).

## Run
```bash
pip install -r requirements.txt
python Double_Pendulum_Simulator.py
```
Requires Python 3.7+.

## Try this
Change an initial angle by a tiny amount and compare runs. The paths diverge quickly, which is the sensitive dependence on initial conditions that makes the system chaotic.
