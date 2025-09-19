#!/usr/bin/env python3
"""
plot_growth.py

Plot V(t) = V0 * 2^(t/dt) and mark the target volume.
Saves figure to figures/growth.png

Usage:
  python plot_growth.py
  python plot_growth.py --V0 1.13e-4 --V 3.81e38 --dt 5
"""
import os
import math
import argparse
import numpy as np
import matplotlib.pyplot as plt

def compute_T(dt, V0, V):
    return dt * math.log(V / V0, 2)

def human_time(minutes):
    hours = minutes / 60.0
    days = hours / 24.0
    return minutes, hours, days

def main():
    p = argparse.ArgumentParser(description="Plot exponential bun growth")
    p.add_argument("--V0", type=float, default=1.13e-4, help="Initial bun volume (m^3)")
    p.add_argument("--V", type=float, default=3.81e38, help="Target volume (m^3)")
    p.add_argument("--dt", type=float, default=5.0, help="Doubling interval (minutes)")
    p.add_argument("--out", type=str, default="figures/growth.png", help="Output PNG path")
    args = p.parse_args()

    V0 = args.V0
    Vtarget = args.V
    dt = args.dt
    outpath = args.out

    if V0 <= 0 or Vtarget <= 0 or dt <= 0:
        raise SystemExit("V0, V and dt must be positive numbers.")

    # compute time to reach the target
    T = compute_T(dt, V0, Vtarget)
    Tmin, Thr, Tdays = human_time(T)

    # build time axis: 0 .. max( T*1.05, 60 min )
    t_max = max(T * 1.05, 60.0)
    t = np.linspace(0, t_max, 1000)
    Vt = V0 * 2**(t / dt)

    # prepare figure
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    plt.figure(figsize=(10,6))
    plt.plot(t, Vt, label=r"$V(t)=V_0\;2^{t/dt}$")
    # horizontal target line
    plt.axhline(Vtarget, color='C1', linestyle='--', label='Target volume')
    # vertical line at T
    plt.axvline(T, color='C2', linestyle='--', label=f"T = {Tmin:.1f} min")
    # annotate T
    plt.annotate(f"T ≈ {Tmin:.1f} min\n({Thr:.2f} hr, {Tdays:.3f} days)",
                 xy=(T, Vtarget),
                 xytext=(T*0.6, Vtarget*1e-3 if Vtarget>0 else 0),
                 arrowprops=dict(arrowstyle="->", color="black"),
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))

    plt.yscale('log')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Volume (m³) — log scale")
    plt.title("Chestnut bun exponential growth")
    plt.grid(True, which="both", ls="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()

    print(f"Saved plot to {outpath}")
    print(f"T = {Tmin:.3f} minutes ({Thr:.6f} hours, {Tdays:.6f} days)")

if __name__ == "__main__":
    main()
