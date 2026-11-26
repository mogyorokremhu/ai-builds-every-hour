"""Penrose-style tiling substitution counts: thin/thick rhombus (Fibonacci) growth."""


def step(thin: int, thick: int) -> tuple[int, int]:
    """One deflation step: thick -> thick+thin, thin -> thick."""
    return thick, thick + thin


if __name__ == "__main__":
    thin, thick = 0, 1
    print("gen  thin  thick  ratio(thick/thin)")
    for g in range(12):
        ratio = f"{thick / thin:.6f}" if thin else "-"
        print(f"{g:3d} {thin:5d} {thick:6d}  {ratio}")
        thin, thick = step(thin, thick)
    print("ratio -> golden ratio 1.618034")
