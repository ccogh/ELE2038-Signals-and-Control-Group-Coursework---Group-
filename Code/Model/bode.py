"""
Bode plot and stability margin analysis for the closed-loop ball-on-incline system.

Open-loop:   L(s) = C(s) * GH(s)
Closed-loop: T(s) = C(s)*GH(s) / (1 + C(s)*GH(s))

Stability margins:
    Gain margin  (GM) - how much gain can increase before instability
    Phase margin (PM) - target > 45 degrees for good robustness
"""

import numpy as np
import matplotlib.pyplot as plt
import control

from pid import Kp, Ki, Kd, pid_num_den, poles_from_coeffs, characteristic_coeffs, PLANT_NUM, PLANT_DEN       # Kp, Ki, Kd = PID gains


def build_transfer_functions(Kp, Ki, Kd):
    GH = control.tf(PLANT_NUM, PLANT_DEN)

    # pid_num_den returns numerator and denominator of C(s) as numpy arrays
    c_num, c_den = pid_num_den(Kp, Ki, Kd)
    C = control.tf(c_num, c_den)

    L = C * GH                                                      # open loop trasnfer func: C(s)*GH(s)

    return L


# open loop transfer func, gain margin, phase margin, phase crossover freq, gain crossover freq
def print_margins(L, gm, pm, wpc, wgc):                             # Prints L(s), closed-loop poles, and stability margins to console
             
    gm_dB = 20 * np.log10(gm) if gm > 0 else float("inf")


    print("=" * 50)
    print("Open-loop transfer function L(s) = C(s)*GH(s)")
    print("=" * 50)
    print(L)

    print("\nClosed-loop poles:")
    cl_poles = poles_from_coeffs(characteristic_coeffs(Kp, Ki, Kd))
    for p in sorted(cl_poles, key = lambda x: x.real):
        print(f"  s = {p:.4f}")

    print("\nStability margins:")
    print(f"  Gain margin  (GM) = {gm:.3f}  ({gm_dB:.2f} dB)  at w = {wpc:.2f} rad/s")
    print(f"  Phase margin (PM) = {pm:.2f} degrees  at w = {wgc:.2f} rad/s")

    
    print("\nStability assessment:")                                # assess robustness against 45 degree target
    if pm > 45:
        print(f"  PM = {pm:.1f} deg > 45 deg : satisfactory robustness")
    elif pm > 0:
        print(f"  PM = {pm:.1f} deg : stable but below 45 deg target, limited robustness")
    else:
        print(f"  PM = {pm:.1f} deg : unstable or marginally stable")

    if gm > 1:
        print(f"  GM = {gm_dB:.1f} dB > 0 dB : stable gain margin")
    else:
        print(f"  GM = {gm_dB:.1f} dB : gain margin indicates instability")


def plot_bode(L, gm, pm, wpc, wgc):                                          # Plots Bode diagram of L(s)

    
    omega = np.logspace(-1, 5, 2000)                                         # Frequency range

    
    mag, phase, omega_out = control.bode(L, omega, plot = False)               # Returns magnitude (linear), phase (radians), frequency

    # convert to dB and degrees for plot
    mag_dB = 20 * np.log10(mag)
    phase_deg = np.degrees(phase)

    fig, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize = (10, 8), sharex = True)

    # magnitude plot
    ax_mag.semilogx(omega_out, mag_dB, color = "tab:blue", linewidth = 1.5)
    ax_mag.axhline(0, color = "black", linewidth = 0.8, linestyle = "--", label = "0 dB")
    ax_mag.set_ylabel("Magnitude [dB]")
    ax_mag.set_title("Bode plot - open-loop L(s) = C(s)*GH(s)")
    ax_mag.grid(True, which = "both", alpha = 0.4)
    ax_mag.legend(loc = "upper left")

    if wgc is not None and not np.isnan(wgc):                               # Marks gain crossover frequency
        ax_mag.axvline(wgc, color = "tab:orange", linewidth = 1, linestyle = ":",
                       label = f"wgc = {wgc:.2f} rad/s")
        ax_mag.legend(loc = "upper left")


    # phase plot
    ax_phase.semilogx(omega_out, phase_deg, color = "tab:red", linewidth = 1.5)
    ax_phase.axhline(-180, color = "black", linewidth = 0.8, linestyle = "--", label = "-180 deg")
    ax_phase.set_ylabel("Phase [degrees]")
    ax_phase.set_xlabel("Frequency [rad/s]")
    ax_phase.grid(True, which = "both", alpha = 0.4)
    ax_phase.legend(loc = "upper left")

    if wpc is not None and not np.isnan(wpc):                               # Marks phase crossover frequency
        ax_phase.axvline(wpc, color = "tab:green", linewidth = 1, linestyle = ":",
                         label = f"wpc = {wpc:.2f} rad/s")
        ax_phase.legend(loc = "upper left")


    if wgc is not None and not np.isnan(wgc):                               # annotate phase margin at the correct point on the phase curve
        idx = np.argmin(np.abs(omega_out - wgc))
        phase_at_wgc = phase_deg[idx]
        ax_phase.annotate(
            f"PM = {pm:.1f} deg",
            xy = (wgc, phase_at_wgc),
            xytext = (wgc * 5, phase_at_wgc + 30),
            arrowprops = dict(arrowstyle = "->", color = "tab:orange"),
            color = "tab:orange",
            fontsize = 9,
        )

    plt.tight_layout()
    plt.savefig("bode_plot.svg")
    plt.show()
    print("\nBode plot saved to bode_plot.svg")


if __name__ == "__main__":
    L = build_transfer_functions(Kp, Ki, Kd)
    gm, pm, wpc, wgc = control.margin(L)
    print_margins(L, gm, pm, wpc, wgc)
    plot_bode(L, gm, pm, wpc, wgc)