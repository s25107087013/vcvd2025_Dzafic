Tyre Force Simulation (s2510787013.py)
==============================

What this is
------------
This project computes simplified tyre forces using a Pacejka/Magic-Formula style model:
- Longitudinal force Fx (braking/traction) as a function of longitudinal slip
- Lateral force Fy as a function of slip angle (alpha)
- A simple "friction-ellipse" style reduction is applied so Fy decreases when Fx uses more
  of the tyre's available grip.

The script also plots Fx and Fy versus longitudinal slip (%).

Files
-----
- s2510787013.py: the simulation + plotting script
- .venv/: local Python virtual environment (created on this machine)

Requirements
------------
- Python 3.x
- numpy
- matplotlib
- scipy (for g = 9.81... m/s^2)

If you are using the included virtual environment, run Python from:
  .\.venv\Scripts\python.exe

How to run
----------
Open PowerShell in this folder:
  E:\MASTER AMM\1st semestar\code

Mode 1: Interactive (type values when prompted)
  .\.venv\Scripts\python.exe .\s2510787013.py

Mode 2: Command-line flags (no prompts)
  .\.venv\Scripts\python.exe .\s2510787013.py --weight 4050 --slip 1.4 --mu 1.0

Arguments
---------
--weight  Vehicle mass [kg]. The model assumes 4 equal wheels.
--slip    Slip angle alpha (units depend on the coefficient set used in the model).
--mu      Tyre-road friction coefficient (dimensionless).

What the output means
---------------------
- The terminal prints the chosen weight and the per-wheel vertical load Fz (in kN).
- A plot window opens:
  - Fx (solid line) vs longitudinal slip (%)
  - Fy (dashed line) vs longitudinal slip (%), reduced by the friction-ellipse approximation

Notes / Assumptions
-------------------
- Fz is computed per wheel as (weight * g / 4) and converted to kN.
- The coefficient sets (a1..a8) are taken as given in the script.
- Camber gamma is assumed 0 (no lateral force shifts from camber).
- The friction-ellipse reduction is: Fy_combined = Fy_pure * sqrt(1 - (Fx/Dx)^2),
  with Fx/Dx clamped to [-1, 1].

Troubleshooting
---------------
- "Missing module numpy/matplotlib/scipy":
  Install dependencies into the environment you are using, or recreate the venv.

- The plot window does not appear / script exits immediately:
  Run it from a normal terminal (not a restricted runner) and ensure matplotlib is installed.

- To see help:
  .\.venv\Scripts\python.exe .\s2510787013.py -h
