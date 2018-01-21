def Hue(R, G, B, deg = False):
    MIN = min(R, G, B)
    MAX = max(R, G, B)
    delta = MAX - MIN

    if delta == 0:
        return 0
    H = 0
    if MAX == R:
        H = 0 + (G - B) / delta
    if MAX == G:
        H = 2 + (B - R) / delta
    if MAX == B:
        H = 4 + (R - G) / delta

    if (deg):
        H *= 60
        while H < 0:
            H += 360
    else:
        H /= 6
        while H < 0:
            H += 1
    return H


def SaturationHSV(R, G, B):
    MIN = min(R, G, B)
    MAX = max(R, G, B)

    if MAX == 0:
        return 0
    return (MAX - MIN) / MAX

def SaturationHSL(R, G, B):
    MIN = min(R, G, B)
    MAX = max(R, G, B)

    if MAX == 0:
        return 0
    if MIN == 1:
        return 0
    return (MAX - MIN) / (1 - abs(MAX + MIN - 1))

def Value(R, G, B):
    return max(R, G, B)

def Brightness(R, G, B):
    return (Value(R, G, B))

def Luminance(R, G, B):
    MIN = min(R, G, B)
    MAX = max(R, G, B)
    return (MAX + MIN) / 2

def Intensity(R, G, B):
    return 1 / 3 * (R + G + B)

R = 0.4
G = 0.4
B = 0.4

print(Hue(R, G, B))
print(SaturationHSV(R, G, B))
print(SaturationHSL(R, G, B))
print(Value(R, G, B))
print(Luminance(R, G, B))
print(Intensity(R, G, B))