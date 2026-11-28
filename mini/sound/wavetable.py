"""Wavetable synth: morph between sine, triangle and square tables with linear interpolation. Usage: python wavetable.py [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050
N = 256
SINE = [math.sin(2 * math.pi * i / N) for i in range(N)]
TRI = [1 - 4 * abs(i / N - 0.5) for i in range(N)]
SQUARE = [1.0 if i < N // 2 else -1.0 for i in range(N)]
TABLES = (SINE, TRI, SQUARE)


def lookup(table: list[float], phase: float) -> float:
    """Linearly interpolated table read; phase in [0, 1)."""
    x = phase * N
    i = int(x) % N
    frac = x - int(x)
    return table[i] * (1 - frac) + table[(i + 1) % N] * frac


def render(freq: float = 196.0, secs: float = 4.0) -> list[int]:
    out = []
    total = int(RATE * secs)
    for i in range(total):
        t = i / RATE
        pos = i / total * (len(TABLES) - 1)
        k = min(int(pos), len(TABLES) - 2)
        m = pos - k
        phase = (t * freq) % 1.0
        s = lookup(TABLES[k], phase) * (1 - m) + lookup(TABLES[k + 1], phase) * m
        out.append(int(s * 12000))
    return out


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "wavetable.wav"
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in render()))
    print("wrote", path)
