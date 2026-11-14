"""FM synthesis bell: a carrier modulated by a decaying modulator. Usage: python fm_bell.py [freq_hz] [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050


def bell(freq: float, secs: float = 2.0, ratio: float = 3.5, index: float = 5.0) -> list[int]:
    n = int(RATE * secs)
    out = []
    for i in range(n):
        t = i / RATE
        env = math.exp(-3 * t)
        mod = index * env * math.sin(2 * math.pi * freq * ratio * t)
        out.append(int(14000 * env * math.sin(2 * math.pi * freq * t + mod)))
    return out


if __name__ == "__main__":
    f = float(sys.argv[1]) if len(sys.argv) > 1 else 440.0
    path = sys.argv[2] if len(sys.argv) > 2 else "fm_bell.wav"
    samples = bell(f)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))
    print("wrote", path, len(samples), "samples")
