"""ADSR envelope demo: a plucked and a pad-like note. Usage: python envelope.py [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050


def adsr(n: int, a: float, d: float, s: float, r: float) -> list[float]:
    """Return n envelope values (attack/decay/release as fractions, s = sustain level)."""
    out = []
    for i in range(n):
        t = i / n
        if t < a:
            v = t / a
        elif t < a + d:
            v = 1 - (1 - s) * (t - a) / d
        elif t < 1 - r:
            v = s
        else:
            v = s * (1 - t) / r
        out.append(max(v, 0.0))
    return out


def note(freq: float, secs: float, env: tuple[float, float, float, float]) -> list[int]:
    n = int(RATE * secs)
    e = adsr(n, *env)
    return [int(12000 * e[i] * math.sin(2 * math.pi * freq * i / RATE)) for i in range(n)]


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "envelope.wav"
    samples = note(440, 0.8, (0.01, 0.3, 0.1, 0.4)) + note(330, 1.2, (0.4, 0.2, 0.7, 0.3))
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))
    print("wrote", path)
