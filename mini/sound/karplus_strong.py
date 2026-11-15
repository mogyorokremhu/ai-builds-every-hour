"""Karplus-Strong plucked string: a noise burst fed through a decaying delay-line average. Usage: python karplus_strong.py [out.wav]"""
import random
import struct
import sys
import wave

RATE = 22050


def pluck(freq: float, secs: float = 1.5, decay: float = 0.996) -> list[float]:
    n = int(RATE / freq)
    buf = [random.uniform(-1, 1) for _ in range(n)]
    out = []
    for i in range(int(RATE * secs)):
        j = i % n
        out.append(buf[j])
        buf[j] = decay * 0.5 * (buf[j] + buf[(j + 1) % n])
    return out


if __name__ == "__main__":
    random.seed(1)
    path = sys.argv[1] if len(sys.argv) > 1 else "karplus.wav"
    notes = [196.0, 246.94, 293.66, 392.0]
    mix: list[float] = []
    for k, f in enumerate(notes):
        mix += [0.0] * (RATE // 4) if k else []
        mix += pluck(f, 1.0)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s)) * 12000)) for s in mix))
    print("wrote", path)
