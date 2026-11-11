"""Synthesized kick/snare/hat drum loop. Usage: python drum_beat.py [bpm] [out.wav]"""
import math
import random
import struct
import sys
import wave

RATE = 22050


def kick() -> list[float]:
    n = int(RATE * 0.25)
    return [math.sin(2 * math.pi * (50 + 100 * math.exp(-i / 800)) * i / RATE) * math.exp(-5 * i / n) for i in range(n)]


def snare() -> list[float]:
    n = int(RATE * 0.18)
    return [random.uniform(-1, 1) * math.exp(-6 * i / n) * 0.7 for i in range(n)]


def hat() -> list[float]:
    n = int(RATE * 0.05)
    return [random.uniform(-1, 1) * math.exp(-10 * i / n) * 0.3 for i in range(n)]


def render(bpm: float = 110.0, bars: int = 2) -> list[int]:
    step = int(RATE * 60 / bpm / 2)  # eighth notes
    pattern = ["k h", "h", "s h", "h"] * 2  # per eighth: kick/snare/hat flags
    buf = [0.0] * (step * len(pattern) * bars + RATE)
    for b in range(bars):
        for j, cell in enumerate(pattern):
            pos = (b * len(pattern) + j) * step
            for ch in cell.split():
                for i, v in enumerate({"k": kick(), "s": snare(), "h": hat()}[ch]):
                    buf[pos + i] += v
    return [int(max(-1, min(1, v)) * 14000) for v in buf]


if __name__ == "__main__":
    random.seed(1)
    bpm = float(sys.argv[1]) if len(sys.argv) > 1 else 110.0
    path = sys.argv[2] if len(sys.argv) > 2 else "drums.wav"
    s = render(bpm)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", x) for x in s))
    print("wrote", path, len(s), "samples")
