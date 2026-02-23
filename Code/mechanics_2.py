import math

#Coursework parameters (SI units)
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
        print("WARNING: i0^2 < 0 (no real equilibrium current) for this x0 with the chosen force directions.")
        print(f"i0^2 = {i0_sq:.6g}. Try choosing x0 > d (spring stretched) and x0 < delta.")
        return float("nan")

    return math.sqrt(i0_sq)

if __name__ == "__main__":
    for x0 in [0.40, 0.43, 0.44]:
        i0 = i0_from_x0(x0)
        print(f"x0 = {x0:.2f} m  =>  i0 = {i0:.4f} A")
