"""A circle filled with a checkerboard, drawn in ASCII."""
R = 12
for y in range(-R, R + 1):
    row = ""
    for x in range(-2 * R, 2 * R + 1):
        if (x / 2) ** 2 + y ** 2 <= R ** 2:
            row += "#" if ((x // 4) + (y // 2)) % 2 == 0 else "."
        else:
            row += " "
    print(row)
