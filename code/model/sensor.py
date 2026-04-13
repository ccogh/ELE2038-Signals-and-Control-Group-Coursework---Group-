# Sensor output model: y = Km * x
def sensor_output(x, i, p):
    return p["Km"] * x

