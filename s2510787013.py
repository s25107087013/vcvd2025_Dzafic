"""Tire Force Simulation Script

This program computes longitudinal and lateral tire forces
using a simplified Pacejka-based model. It evaluates how
forces change with increasing slip.

Author: Dzafic Isak B.Sc. - s2510787013
Date: 23-03-2026
Version: 1.0

References:
1. Pacejka, H. B. (1987). Tire and Vehicle Dynamics
2. Genta, G. (2005). The Automotive Chassis: Volume 1: Components Design
3. Course assignment material
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import g 

def side_force(alpha: float, weight: float, mu: float):
    """
    Compute lateral tire force Fy using a simplified Pacejka model.

    Args:
        alpha: Slip angle (rad or deg depending on the coefficient set used).
        weight: Vehicle mass [kg]. Model assumes 4 equal wheels.
        mu: Tyre-road friction coefficient.

    Returns:
        (Fy, D) where:
        Fy: lateral force (same force unit as the coefficient set).
        D: peak factor (maximum lateral force in the model for this load/mu).
    """
    # Per-wheel vertical load. Converted to kN because this coefficient set expects Fz in kN.
    Fz = ((weight * g) / 4) / 1000

    # Coefficients for the lateral force model.
    a1y = -22.1
    a2y = 1011
    a3y = 1078
    a4y = 1.82
    a5y = 0.208
    a6y = 0.000
    a7y = -0.354
    a8y = 0.707
    
    # Magic Formula parameters
    D = (a1y * Fz**2 + a2y * Fz) * mu  # peak factor (max force for this load/mu)
    C = 1.30  # shape factor
    B = (a3y * Fz**2 + a4y * Fz) / (C * D * np.exp(a5y * Fz))  # stiffness factor
    E = a6y * Fz**2 + a7y * Fz + a8y  # curvature factor

    # We assume camber gamma = 0, so horizontal/vertical shifts are 0 in this simplified model.
    delta_Sh = 0
    delta_Sv = 0

    alpha_eff = alpha + delta_Sh
    phi = (1 - E) * alpha_eff + (E / B) * np.arctan(B * alpha_eff)
    
    side_force = D * np.sin(C * np.arctan(B * phi)) + delta_Sv
    
    return side_force, D  



def brake_force(kappa: float, weight: float, mu: float):
    """
    Compute longitudinal tire force Fx using a simplified Pacejka model.

    Args:
        kappa: Longitudinal slip input used by the model (here: slip_percent from 0..100).
        weight: Vehicle mass [kg]. Model assumes 4 equal wheels.
        mu: Tyre-road friction coefficient.

    Returns:
        (Fx, D) where:
        Fx: longitudinal force (same force unit as the coefficient set).
        D: peak factor (maximum longitudinal force in the model for this load/mu).
    """
    Fz = ((weight * g) / 4) / 1000

    # Coefficients for the longitudinal force model.
    a1x = -21.3
    a2x = 1144
    a3x = 49.6
    a4x = 226
    a5x = 0.069
    a6x = -0.006
    a7x = 0.056
    a8x = 0.486

    # Magic Formula parameters.
    D = (a1x * Fz**2 + a2x * Fz) * mu  # peak factor
    C = 1.65  # shape factor
    B = (a3x * Fz**2 + a4x * Fz) / (C * D * np.exp(a5x * Fz))  # stiffness factor
    E = a6x * Fz**2 + a7x * Fz + a8x
    phi = (1 - E) * kappa + (E / B) * np.arctan(B * kappa)
    brake_force = D * np.sin(C * np.arctan(B * phi))
    
    return brake_force, D 

def main():
    """
    Entry point.

    Supports two usage styles:
    1) CLI flags: `--weight --slip --mu`
    2) Interactive prompts: run with no flags and type values in the terminal.
    """
    
    parser = argparse.ArgumentParser(description='Process some values.')
    parser.add_argument('--weight', type=float, required=False, help='Vehicle weight in kg')
    parser.add_argument('--slip', type=float, required=False, help='Slip angle (alpha)')
    parser.add_argument('--mu', type=float, required=False, help='Friction coefficient')
    
    args = parser.parse_args()

    def _prompt_float(label: str) -> float:
        while True:
            try:
                raw = input(f"{label}: ").strip()
            except (EOFError, KeyboardInterrupt):
                raise SystemExit("\nInput cancelled. Re-run and enter the values when prompted, or pass --weight/--slip/--mu.")
            try:
                return float(raw)
            except ValueError:
                print("Please enter a number (example: 4050 or 1.4).")

    # If user didn't pass flags, ask interactively in the terminal (slip, then weight, then mu).
    if args.slip is None:
        args.slip = _prompt_float("Enter slip angle alpha")
    if args.weight is None:
        args.weight = _prompt_float("Enter vehicle weight [kg]")
    if args.mu is None:
        args.mu = _prompt_float("Enter friction coefficient mu")

    # Show the chosen inputs and the per-wheel vertical load used by the model.
    Fz_print = ((args.weight * g) / 4) / 1000
    print(f"Weight: {args.weight} kg (Fz={Fz_print:.2f} kN)")

    x_values = np.linspace(0, 100, 100)  # slip percent values from 0..100
    brake_force_list = []
    side_force_list = []

    # Loop through slip values and combine Fx/Fy using a simple friction-ellipse approximation.
    # Idea: as longitudinal force approaches its peak, available lateral force is reduced.
    for slip_percent in x_values:
        fx_pure, D_x = brake_force(slip_percent, args.weight, args.mu) 
        fy_pure, _D_y = side_force(args.slip, args.weight, args.mu)

        if D_x == 0:
            utilization = 0
        else:
            utilization = fx_pure / D_x  # ratio of used longitudinal capacity
        if utilization > 1:
            utilization = 1
        if utilization < -1:
            utilization = -1
            
        reduction_factor = np.sqrt(1 - utilization**2)  # remaining lateral capacity (0..1)
        
        fy_combined = fy_pure * reduction_factor
        
        brake_force_list.append(fx_pure)
        side_force_list.append(fy_combined)


    # Plot: Fx and the reduced Fy vs slip percent.
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_values, brake_force_list, label='Brake Force Fx', linewidth=2.0)
    ax.plot(x_values, side_force_list, label='Side Force Fy', linewidth=2.0, linestyle='--')

    ax.set_title(f"Tire Forces vs Longitudinal Slip (Alpha={args.slip} )")
    ax.set_xlabel("Longitudinal slip x [%]")
    ax.set_ylabel("Force [N]")

    ax.set_xlim(0, 100)
    ax.set_ylim(bottom=0)
    ax.legend()
    ax.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
# Example:
#   python s2510787013.py --weight 4050 --slip 1.4 --mu 1.0
