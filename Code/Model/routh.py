from __future__ import annotations

import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

from pid import (
    characteristic_coeffs,
    is_bibo_stable_from_poly,
    poles_from_coeffs,
    pretty_polynomial,
    closed_loop_num_den,
)


def routh_table(coeffs: np.ndarray, eps: float = 1e-9) -> np.ndarray:
    """
    Notes:
    - If the first element of a row is zero, a small epsilon is used for numerical testing.
    """
    coeffs = np.asarray(coeffs, dtype=float)
    n = len(coeffs) - 1
    cols = int(np.ceil((n + 1) / 2))

    table = np.zeros((n + 1, cols), dtype=float)

    #first two rows
    table[0, :len(coeffs[0::2])] = coeffs[0::2]
    table[1, :len(coeffs[1::2])] = coeffs[1::2]

    for i in range(2, n + 1):
        #Handle all zero previous row using the auxiliary polynomial method
        if np.allclose(table[i - 1, :], 0.0, atol=eps):
            power = n - (i - 2)
            deriv = []
            current_power = power

            for value in table[i - 2, :]:
                if current_power > 0:
                    deriv.append(value * current_power)
                current_power -= 2

            table[i - 1, :len(deriv)] = deriv

        # Handle zero leading element numerically
        if abs(table[i - 1, 0]) < eps:
            table[i - 1, 0] = eps

        for j in range(cols - 1):
            a = table[i - 1, 0]
            b = table[i - 2, 0]
            c = table[i - 2, j + 1]
            d = table[i - 1, j + 1]
            table[i, j] = (a * c - b * d) / a

    return table


def first_column_sign_changes(table: np.ndarray, eps: float = 1e-9) -> int:
    """
    Count sign changes in the first column of the Routh table.
    For generic cases, this equals the number of right-half-plane roots.
    """
    col = table[:, 0].copy()
    col[np.abs(col) < eps] = 0.0

    signs = []
    for value in col:
        if value > 0:
            signs.append(1)
        elif value < 0:
            signs.append(-1)

    return sum(1 for i in range(len(signs) - 1) if signs[i] != signs[i + 1])


def print_routh_table(table: np.ndarray) -> None:
    """Pretty-print the Routh table."""
    degree = table.shape[0] - 1
    print("Routh table:")
    for i, row in enumerate(table):
        power = degree - i
        values = "  ".join(f"{x:14.6g}" for x in row)
        print(f"s^{power:<2}: {values}")


def analyse_trial(Kp: float, Ki: float, Kd: float) -> None:
    """
    Print the characteristic polynomial, Routh table, sign changes,
    direct root check, and BIBO stability result.
    """
    coeffs = characteristic_coeffs(Kp, Ki, Kd)
    table = routh_table(coeffs)
    changes = first_column_sign_changes(table)
    poles = poles_from_coeffs(coeffs)

    print(f"Trial gains: Kp={Kp}, Ki={Ki}, Kd={Kd}\n")
    print("Characteristic polynomial:")
    print("Q(s) =", pretty_polynomial(coeffs))
    print()
    print_routh_table(table)
    print("\nFirst column:", table[:, 0])
    print("Sign changes in first column:", changes)

    if changes == 0:
        print("Routh result: no right-half-plane roots indicated.")
    else:
        print(f"Routh result: unstable, with {changes} right-half-plane root(s) indicated.")

    print("\nDirect root check:")
    for p in poles:
        print(f"  {p.real: .6f}{p.imag:+.6f}j")

    print("\nBIBO stable from roots?", "Yes" if is_bibo_stable_from_poly(coeffs) else "No")


def plot_responses(Kp: float, Ki: float, Kd: float, t_end: float = 5.0, num_points: int = 2000) -> None:
    """
    Plot:
      1) closed-loop output step response y(t)
      2) approximate control signal u(t)

    Notes:
    - y(t) is obtained from the closed-loop transfer function T(s) = Y(s)/R(s)
    - u(t) is reconstructed in the time domain as:
          u(t) ≈ Kp*e(t) + Ki*∫e(t)dt - Kd*dy/dt
      where e(t) = r(t) - y(t)
    - This avoids the improper-transfer-function issue caused by the ideal derivative term.
    """
    # Closed-loop output transfer function Y(s)/R(s)
    y_num, y_den = closed_loop_num_den(Kp, Ki, Kd)
    y_sys = signal.TransferFunction(y_num, y_den)

    # Time vector
    t = np.linspace(0.0, t_end, num_points)

    # Unit-step output response
    t_y, y = signal.step(y_sys, T=t)

    # Reference input
    r = np.ones_like(t_y)

    # Error
    e = r - y

    # Numerical integration of the error
    dt = t_y[1] - t_y[0]
    e_int = np.cumsum(e) * dt

    # Numerical derivative of the output
    y_dot = np.gradient(y, t_y)

    # Approximate control signal
    # Using derivative on measurement avoids the ideal impulse from d/dt(step)
    u = Kp * e + Ki * e_int - Kd * y_dot

    # Basic response metrics
    final_value = y[-1]
    peak_value = np.max(y)
    overshoot = 0.0
    if abs(final_value) > 1e-12:
        overshoot = max(0.0, (peak_value - final_value) / abs(final_value) * 100.0)

    print("\nStep-response summary:")
    print(f"  Final output value (approx): {final_value:.6f}")
    print(f"  Peak output value:           {peak_value:.6f}")
    print(f"  Percent overshoot:           {overshoot:.2f}%")
    print(f"  Peak control signal:         {np.max(u):.6f}")
    print(f"  Min control signal:          {np.min(u):.6f}")

    # Plot both in one figure window
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Output response
    axes[0].plot(t_y, y, label="Output y(t)")
    axes[0].axhline(1.0, linestyle="--", linewidth=1.0, label="Reference r(t)=1")
    axes[0].set_ylabel("Output")
    axes[0].set_title(f"Closed-loop responses (Kp={Kp}, Ki={Ki}, Kd={Kd})")
    axes[0].grid(True)
    axes[0].legend()

    # Control signal
    axes[1].plot(t_y, u, label="Approx. control signal u(t)")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Control effort")
    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout()

    # Save a copy in case a GUI window does not appear
    filename = f"response_Kp_{Kp:g}_Ki_{Ki:g}_Kd_{Kd:g}.svg"
    plt.savefig(filename)
    print(f"\nSaved plot to: {filename}")
    plt.show()


def main(
    Kp: float = 20000,
    Ki: float = 5000,
    Kd: float = 50,
    plot: bool = True,
    t_end: float = 5.0,
    use_cli: bool = False,
) -> None:
    """
    Run the Routh analysis and, optionally, the plots.

    Default behaviour:
    - good for IDE use: just press Run
    - uses the default gains above
    - plots automatically

    Optional behaviour:
    - set use_cli=True below if you want command-line arguments instead
    """
    if use_cli:
        parser = argparse.ArgumentParser(description="Routh test for trial PID gains.")
        parser.add_argument("--kp", type=float, default=Kp, help="Proportional gain")
        parser.add_argument("--ki", type=float, default=Ki, help="Integral gain")
        parser.add_argument("--kd", type=float, default=Kd, help="Derivative gain")
        parser.add_argument("--plot", action="store_true", help="Plot responses")
        parser.add_argument("--tend", type=float, default=t_end, help="End time for plots")
        args = parser.parse_args()

        Kp = args.kp
        Ki = args.ki
        Kd = args.kd
        plot = args.plot
        t_end = args.tend

    analyse_trial(Kp, Ki, Kd)

    if plot:
        plot_responses(Kp, Ki, Kd, t_end=t_end)


if __name__ == "__main__":
    main(
        Kp=20000,
        Ki=5000,
        Kd=50,
        plot=True,
        t_end=5.0,
        use_cli=False,   
    )