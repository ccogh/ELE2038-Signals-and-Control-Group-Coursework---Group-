import math
import matplotlib.pyplot as plt

# oursework parameters (SI units)
m = 0.462
g = 9.81
phi = math.radians(41.0)
k = 1885.0
d = 0.42
delta = 0.65
c = 6.811e-3


def i0_from_x0(x0: float) -> float:
    gap = delta - x0
    if gap <= 0:
        raise ValueError(f"x0 must be < delta (magnet). Got x0={x0}, delta={delta}")

    i0_sq = (k * (x0 - d) - m * g * math.sin(phi)) * (gap ** 2) / c

    if i0_sq < 0:
        raise ValueError(
            f"No real equilibrium current for x0={x0:.6f} m "
            f"(i0^2 = {i0_sq:.6f} < 0)"
        )

    return math.sqrt(i0_sq)


def operating_point_limits():
    """
    Valid operating points require:
      1) x0 < delta
      2) k(x0 - d) - m g sin(phi) >= 0

    So:
      x0 >= d + (m g sin(phi))/k
      x0 < delta
    """
    x0_min = d + (m * g * math.sin(phi)) / k
    x0_max = delta
    return x0_min, x0_max


def is_valid_x0(x0: float) -> bool:
    x0_min, x0_max = operating_point_limits()
    return (x0 >= x0_min) and (x0 < x0_max)


if __name__ == "__main__":
    x0_min, x0_max = operating_point_limits()

    print("VALID OPERATING-POINT RANGE")
    print("-" * 40)
    print(f"Continuous range: {x0_min:.6f} m <= x0 < {x0_max:.6f} m")

    #2 d.p. values
    two_dp_points = [round(0.40 + 0.01 * i, 2) for i in range(26)]  # 0.40 to 0.65
    valid_2dp = [x for x in two_dp_points if is_valid_x0(x)]

    print("\nValid x0 values to 2 d.p.:")
    print(valid_2dp)

    if valid_2dp:
        print(f"\nSmallest valid x0 at 2 d.p. = {valid_2dp[0]:.2f} m")
        print(f"Largest valid x0 at 2 d.p.  = {valid_2dp[-1]:.2f} m")

    print("\nCURRENT REQUIRED AT EACH TEST POINT")
    print("-" * 40)

    test_points = [0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48,
                   0.50, 0.52, 0.54, 0.56, 0.58, 0.60, 0.62, 0.64]

    for x0 in test_points:
        try:
            i0 = i0_from_x0(x0)
            print(f"x0 = {x0:.2f} m  =>  i0 = {i0:.4f} A   [VALID]")
        except ValueError as e:
            print(f"x0 = {x0:.2f} m  =>  INVALID ({e})")

    #Generate many x0 points across the valid range for plotting
    x_plot = []
    i_plot = []

    num_points = 300
    eps = 1e-6 
    step = (x0_max - eps - x0_min) / (num_points - 1)

    for n in range(num_points):
        x0 = x0_min + n * step
        try:
            i0 = i0_from_x0(x0)
            x_plot.append(x0)
            i_plot.append(i0)
        except ValueError:
            pass

    #Plot i0 versus x0
    plt.figure(figsize=(8, 5))
    plt.plot(x_plot, i_plot, linewidth=2)
    plt.xlabel("Operating point x0 (m)")
    plt.ylabel("Equilibrium current i0 (A)")
    plt.title("Equilibrium current required vs operating point")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
