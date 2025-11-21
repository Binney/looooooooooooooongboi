def lerp(a, b, x):
    return a + (b - a) * x

def colour_interp(col1, col2, x):
    (r1, g1, b1) = col1
    (r2, g2, b2) = col2
    return (lerp(r1, r2, x), lerp(g1, g2, x), lerp(b1, b2, x))

def palette_interp(palette, x):
    p = len(palette) - 1
    col = int(p * x)
    return colour_interp(palette[col], palette[col + 1], (x - col / p) * p)

def scale_tuple(t, x):
    return tuple(x * tt for tt in t)
