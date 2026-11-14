"""Bitcrusher: reduce bit depth and sample rate of a sweeping saw. Usage: python bitcrush.py [bits] [out.wav]"""
import struct
import sys
import wave

RATE = 22050


def saw_sweep(secs: float = 3.0) -> list[float]:
    out, phase = [], 0.0
    n = int(RATE * secs)
    for i in range(n):
        freq = 110 + 330 * i / n
        phase = (phase + freq / RATE) % 1.0
        out.append(2 * phase - 1)
    return out


def crush(samples: list[float], bits: int, hold: int) -> list[int]:
    levels = 2 ** (bits - 1)
    out, last = [], 0
    for i, s in enumerate(samples):
        if i % hold == 0:
            last = round(s * levels) / levels
        out.append(int(last * 12000))
    return out


if __name__ == "__main__":
    bits = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    path = sys.argv[2] if len(sys.argv) > 2 else "bitcrush.wav"
    samples = crush(saw_sweep(), bits, 4)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))
    print("wrote", path, f"{bits}-bit")
