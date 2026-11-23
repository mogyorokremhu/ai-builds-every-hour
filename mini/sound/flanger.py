"""Flanger: mix a signal with a delayed copy whose delay is swept by an LFO. Usage: python flanger.py [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050


def saw(freq: float, secs: float) -> list[float]:
    return [2 * ((freq * i / RATE) % 1.0) - 1 for i in range(int(RATE * secs))]


def flange(x: list[float], depth_ms: float = 3.0, rate_hz: float = 0.5, base_ms: float = 4.0) -> list[float]:
    out = []
    for i, s in enumerate(x):
        d = (base_ms + depth_ms * math.sin(2 * math.pi * rate_hz * i / RATE)) * RATE / 1000
        j = i - d
        k = int(math.floor(j))
        frac = j - k
        a = x[k] if k >= 0 else 0.0
        b = x[k + 1] if k + 1 >= 0 else 0.0
        out.append(0.5 * s + 0.5 * (a * (1 - frac) + b * frac))
    return out


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "flanger.wav"
    y = flange(saw(110.0, 4.0))
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(8000 * v)) for v in y))
    print("wrote", path, len(y), "samples")
