"""Play-by-WAV: render a melody written as note names ('C4 E4 G4:2 R') to a WAV. Usage: python melody.py [out.wav]"""
import sys
from tones import RATE, tone, write_wav

NOTES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def freq(name: str) -> float:
    """'C#4' -> Hz (A4 = 440)."""
    n = NOTES[name[0]]
    rest = name[1:]
    if rest[0] in "#b":
        n += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    midi = 12 * (int(rest) + 1) + n
    return 440.0 * 2 ** ((midi - 69) / 12)


def render(score: str, beat: float = 0.3, wave_name: str = "triangle") -> list[int]:
    out: list[int] = []
    for tok in score.split():
        name, _, length = tok.partition(":")
        dur = beat * (float(length) if length else 1)
        if name == "R":
            out += [0] * int(RATE * dur)
        else:
            out += tone(freq(name), dur * 0.95, wave_name) + [0] * int(RATE * dur * 0.05)
    return out


TWINKLE = "C4 C4 G4 G4 A4 A4 G4:2 F4 F4 E4 E4 D4 D4 C4:2 R"

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "melody.wav"
    write_wav(path, render(TWINKLE))
    print("wrote", path)
