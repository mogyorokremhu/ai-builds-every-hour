"""Reverse-envelope pluck: a note that swells up and cuts off. Usage: python reverse_reverb.py [freq_hz] [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050


def reversed_pluck(freq: float, secs: float = 1.2) -> list[int]:
    """Plucked decaying sine, then time-reversed so it swells into the attack."""
    n = int(RATE * secs)
    note = [int(12000 * math.exp(-4 * i / n) * math.sin(2 * math.pi * freq * i / RATE)) for i in range(n)]
    return note[::-1]


if __name__ == "__main__":
    freq = float(sys.argv[1]) if len(sys.argv) > 1 else 330.0
    path = sys.argv[2] if len(sys.argv) > 2 else "reverse_reverb.wav"
    samples = reversed_pluck(freq) + reversed_pluck(freq * 1.5)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))
    print("wrote", path, len(samples), "samples")
