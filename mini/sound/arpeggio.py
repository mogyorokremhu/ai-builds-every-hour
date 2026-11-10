"""Arpeggiate a minor-pentatonic scale up and down. Usage: python arpeggio.py [root_hz] [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050
PENTATONIC = [0, 3, 5, 7, 10, 12]


def pluck(freq: float, secs: float = 0.2) -> list[int]:
    n = int(RATE * secs)
    return [int(11000 * math.exp(-6 * i / n) * math.sin(2 * math.pi * freq * i / RATE)) for i in range(n)]


if __name__ == "__main__":
    root = float(sys.argv[1]) if len(sys.argv) > 1 else 220.0
    path = sys.argv[2] if len(sys.argv) > 2 else "arpeggio.wav"
    steps = PENTATONIC + PENTATONIC[-2::-1]
    samples: list[int] = []
    for s in steps:
        samples += pluck(root * 2 ** (s / 12))
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))
    print("wrote", path, len(steps), "notes")
