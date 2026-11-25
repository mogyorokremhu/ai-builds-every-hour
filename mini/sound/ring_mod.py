"""Ring modulation: multiply a tone by a carrier for metallic sidebands. Usage: python ring_mod.py [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050


def ring_mod(freq: float, carrier: float, secs: float = 2.0) -> list[int]:
    """Product of two sines gives sum and difference frequencies (freq +/- carrier)."""
    n = int(RATE * secs)
    return [
        int(12000 * math.sin(2 * math.pi * freq * i / RATE) * math.sin(2 * math.pi * carrier * i / RATE))
        for i in range(n)
    ]


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "ring_mod.wav"
    samples = ring_mod(440.0, 150.0) + ring_mod(440.0, 613.0)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))
    print("wrote", path, len(samples), "samples")
