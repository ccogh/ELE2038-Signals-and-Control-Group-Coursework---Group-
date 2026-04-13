from __future__ import annotations

import numpy as np

# Plant numerator / denominator coefficients in descending powers of s
PLANT_NUM = np.array([142.5], dtype=float)
PLANT_DEN = np.array([0.03, 456.1, 22478.0, 183120.0, -2016000.0], dtype=float)

Kp = 32000.0
Ki = 20000.0
Kd = 1500.0

def pid_num_den(Kp: float, Ki: float, Kd: float):
    """
    Return PID numerator/denominator in descending powers of s.

    C(s) = (Kd s^2 + Kp s + Ki) / s
    """
    num = np.array([Kd, Kp, Ki], dtype=float)
    den = np.array([1.0, 0.0], dtype=float)  # s
    return num, den


def characteristic_coeffs(Kp: float, Ki: float, Kd: float) -> np.ndarray:
    """
    Return the closed-loop characteristic polynomial coefficients
    for a unity-feedback loop with the coursework plant and PID controller.

    Output is descending powers of s.
    """
    # Q(s) = den(C)*den(G) + num(C)*num(G)
    # First term: s * Dp(s)
    first_term = np.convolve([1.0, 0.0], PLANT_DEN)

    # Second term: 142.5 * (Kd s^2 + Kp s + Ki)
    second_term = 142.5 * np.array([Kd, Kp, Ki], dtype=float)

    # Pad the shorter polynomial to add them
    if len(second_term) < len(first_term):
        second_term = np.pad(second_term, (len(first_term) - len(second_term), 0))
    elif len(first_term) < len(second_term):
        first_term = np.pad(first_term, (len(second_term) - len(first_term), 0))

    return first_term + second_term


def open_loop_num_den(Kp: float, Ki: float, Kd: float):
    """
    Return open-loop transfer function L(s) = C(s)G(s).

    Output:
        num, den in descending powers of s
    """
    c_num, c_den = pid_num_den(Kp, Ki, Kd)
    num = np.convolve(c_num, PLANT_NUM)
    den = np.convolve(c_den, PLANT_DEN)
    return num, den


def closed_loop_num_den(Kp: float, Ki: float, Kd: float):
    """
    Return closed-loop transfer function T(s) = L(s)/(1 + L(s))
    for unity feedback.

    Output:
        numerator, denominator in descending powers of s
    """
    ol_num, ol_den = open_loop_num_den(Kp, Ki, Kd)

    a = ol_den.copy()
    b = ol_num.copy()

    if len(b) < len(a):
        b = np.pad(b, (len(a) - len(b), 0))
    elif len(a) < len(b):
        a = np.pad(a, (len(b) - len(a), 0))

    cl_den = a + b
    cl_num = ol_num
    return cl_num, cl_den


def poles_from_coeffs(coeffs: np.ndarray) -> np.ndarray:
    """Return roots/poles of a polynomial with coefficients in descending powers of s."""
    return np.roots(coeffs)


def is_bibo_stable_from_poly(coeffs: np.ndarray, tol: float = 1e-9) -> bool:
    """Check if all polynomial roots lie strictly in the left half-plane."""
    poles = poles_from_coeffs(coeffs)
    return bool(np.all(np.real(poles) < -tol))


def pretty_polynomial(coeffs: np.ndarray, var: str = "s") -> str:
    """Return a readable polynomial string."""
    coeffs = np.asarray(coeffs, dtype=float)
    degree = len(coeffs) - 1
    parts = []

    for i, a in enumerate(coeffs):
        power = degree - i
        if abs(a) < 1e-12:
            continue

        sign = "-" if a < 0 else "+"
        mag = abs(a)

        if power == 0:
            term = f"{mag:.6g}"
        elif power == 1:
            term = f"{mag:.6g}{var}"
        else:
            term = f"{mag:.6g}{var}^{power}"

        parts.append((sign, term))

    if not parts:
        return "0"

    first_sign, first_term = parts[0]
    text = first_term if first_sign == "+" else f"-{first_term}"

    for sign, term in parts[1:]:
        text += f" {sign} {term}"

    return text


def print_trial_summary(Kp: float, Ki: float, Kd: float) -> None:
    """Convenience printer for one trial set of gains."""
    q = characteristic_coeffs(Kp, Ki, Kd)
    poles = poles_from_coeffs(q)

    print(f"Trial gains: Kp={Kp}, Ki={Ki}, Kd={Kd}")
    print("Characteristic polynomial:")
    print("Q(s) =", pretty_polynomial(q))
    print("\nClosed-loop poles:")
    for p in poles:
        print(f"  {p.real: .6f}{p.imag:+.6f}j")
    print("\nBIBO stable?" , "Yes" if is_bibo_stable_from_poly(q) else "No")


if __name__ == "__main__":
    print_trial_summary(Kp, Ki, Kd)