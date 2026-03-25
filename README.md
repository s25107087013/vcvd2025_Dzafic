# Tyre Force Simulation (s2510787013)

## Description
This project implements a simplified tyre model based on the Pacejka “Magic Formula”.  
It computes longitudinal (Fx) and lateral (Fy) forces and includes combined slip behaviour using a friction ellipse approach.

---
## Project Structure
- `s2510787013.py` – Main simulation and plotting script  
- `.venv/` – Local Python virtual environment
- `README.txt` – Project description 
---

## Requirements
Install the required libraries:

pip install numpy matplotlib scipy

---

## Usage

### Run with command-line arguments
python s2510787013.py --weight 4050 --slip 1.4 --mu 1.0
### Parameters
- `--slip`   : Slip angle (alpha)
- `--weight` : Vehicle mass [kg]    
- `--mu`     : Friction coefficient  

---

## Output
- Prints vehicle weight and normal load per wheel  
- Generates a plot of:
  - Longitudinal force (Fx)
  - Lateral force (Fy)

---

## Model Description
- Normal load per wheel: Fz = (weight × g) / 4  
- Empirical coefficients (a1–a8) define tire behaviour  
- Camber angle is assumed zero  
- Combined slip is approximated using a friction ellipse  

Fy_combined = Fy_pure * sqrt(1 - (Fx/Dx)^2)

---

## Troubleshooting
- Missing libraries → install using pip  
- Plot not showing → run in a standard terminal  
- Show help:

python s2510787013.py -h

---

## Author
Isak-2510787013
