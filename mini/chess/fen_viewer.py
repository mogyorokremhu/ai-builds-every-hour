"""Render a FEN string as an ASCII board. Usage: python fen_viewer.py ["FEN"]"""
import sys

START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def parse_fen(fen: str) -> list[list[str]]:
    """Return an 8x8 grid (rank 8 first) of piece letters or '.'."""
    rows = fen.split()[0].split("/")
    if len(rows) != 8:
        raise ValueError("FEN needs 8 ranks")
    grid = []
    for row in rows:
        line: list[str] = []
        for ch in row:
            line.extend("." * int(ch) if ch.isdigit() else ch)
        if len(line) != 8:
            raise ValueError(f"bad rank: {row}")
        grid.append(line)
    return grid


def render(fen: str) -> str:
    grid = parse_fen(fen)
    out = []
    for i, row in enumerate(grid):
        out.append(f"{8 - i} " + " ".join(row))
    out.append("  a b c d e f g h")
    parts = fen.split()
    if len(parts) > 1:
        out.append("White to move" if parts[1] == "w" else "Black to move")
    return "\n".join(out)


if __name__ == "__main__":
    print(render(sys.argv[1] if len(sys.argv) > 1 else START))
