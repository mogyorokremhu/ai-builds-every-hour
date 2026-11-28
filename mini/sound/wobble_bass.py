"""Wobble bass: a saw wave through a one-pole low-pass whose cutoff is swept by an LFO. Usage: python wobble_bass.py [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050


def wobble(freq: float = 55.0, lfo_hz: float = 2.0, secs: float = 4.0) -> list[int]:
    out, y = [], 0.0
    for i in range(int(RATE * secs)):
        t = i / RATE
        saw = 2 * ((t * freq) % 1.0) - 1
        cutoff = 200 + 1800 * (0.5 + 0.5 * math.sin(2 * math.pi * lfo_hz * t))
        a = 1 - math.exp(-2 * math.pi * cutoff / RATE)
        y += a * (saw - y)
        out.append(int(y * 16000))
    return out


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "wobble_bass.wav"
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in wobble()))
    print("wrote", path)
