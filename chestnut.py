#!/usr/bin/env python3
"""
chestnut.py
Compute T for V(t) = V0 * 2^(t/dt) and print results using your variables:
t, dt, T, V0, n, V
"""
import argparse
import math

def compute_n(V0, V):
    # n = number of doublings (real)
    return math.log(V / V0, 2)

def compute_T(dt, V0, V):
    # T = dt * log2(V / V0)
    return dt * math.log(V / V0, 2)

def human_time(minutes):
    hours = minutes / 60.0
    days = hours / 24.0
    return minutes, hours, days

def main():
    p = argparse.ArgumentParser(description="Chestnut bun doubling (V(t)=V0*2^(t/dt))")
    p.add_argument("--V0", type=float, default=1.13e-4, help="Initial bun volume (m^3). Default 1.13e-4")
    p.add_argument("--V", type=float, default=3.81e38, help="Target volume (m^3). Default 3.81e38 (Neptune-bound)")
    p.add_argument("--dt", type=float, default=5.0, help="Doubling interval in minutes. Default 5")
    p.add_argument("--ceil", action="store_true", help="Show integer doublings (ceil) and corresponding T")
    args = p.parse_args()

    V0 = args.V0
    V = args.V
    dt = args.dt

    if V0 <= 0 or V <= 0 or dt <= 0:
        print("V0, V and dt must be positive numbers.")
        return

    # number of doublings (real)
    n = compute_n(V0, V)
    # time (real)
    T = compute_T(dt, V0, V)
    T_min, T_hr, T_days = human_time(T)

    print("\n--- Chestnut problem (your variables) ---\n")
    print(f"V0 (initial single-bun volume) = {V0:.6e} m^3")
    print(f"V  (target volume)            = {V:.6e} m^3")
    print(f"dt (doubling interval)        = {dt} minutes\n")
    print(f"n (required doublings, real)  = {n:.6f}")
    print(f"T (time to reach target, real)= {T_min:.3f} minutes "
          f"({T_hr:.6f} hours, {T_days:.6f} days)\n")

    if args.ceil:
        n_int = math.ceil(n)
        T_int = n_int * dt
        Tint_min, Tint_hr, Tint_days = human_time(T_int)
        print(f"[ceil] n (integer doublings)  = {n_int}")
        print(f"[ceil] T (time with integer)  = {T_int:.3f} minutes "
              f"({Tint_hr:.6f} hours, {Tint_days:.6f} days)\n")

    print("--- end ---\n")

if __name__ == "__main__":
    main()
