"""Feedback echo: a short pluck repeated with decaying delay taps. Usage: python echo.py [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050


def pluck(freq: float, secs: float = 0.25) -> list[float]:
    n = int(RATE * secs)
    return [math.exp(-8 * i / n) * math.sin(2 * math.pi * freq * i / RATE) for i in range(n)]


def echo(x: list[float], delay_s: float = 0.3, feedback: float = 0.55, tail_s: float = 2.0) -> list[float]:
    d = int(RATE * delay_s)
    out = x + [0.0] * int(RATE * tail_s)
    for i in range(d, len(out)):
        out[i] += feedback * out[i - d]
    return out


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "echo.wav"
    y = echo(pluck(440.0))
    peak = max(abs(v) for v in y) or 1.0
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(20000 * v / peak)) for v in y))
    print("wrote", path, len(y), "samples")
