"""Exponential frequency sweep (chirp). Usage: python sweep.py [f0] [f1] [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050


def sweep(f0: float, f1: float, secs: float = 3.0) -> list[int]:
    n = int(RATE * secs)
    k = math.log(f1 / f0)
    out = []
    for i in range(n):
        t = i / RATE
        # phase of exponential chirp: 2*pi*f0*T/k * (e^(k t/T) - 1)
        ph = 2 * math.pi * f0 * secs / k * (math.exp(k * t / secs) - 1)
        out.append(int(12000 * math.sin(ph)))
    return out


if __name__ == "__main__":
    f0 = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0
    f1 = float(sys.argv[2]) if len(sys.argv) > 2 else 2000.0
    path = sys.argv[3] if len(sys.argv) > 3 else "sweep.wav"
    s = sweep(f0, f1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", x) for x in s))
    print("wrote", path, len(s), "samples")
