"""Shepard tone: an endlessly rising illusion built from octave-spaced sines. Usage: python shepard_tone.py [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050


def shepard(secs: float = 8.0, base: float = 55.0, octaves: int = 6) -> list[int]:
    """Each partial glides up one octave per cycle while a bell-shaped gain fades the extremes."""
    n = int(RATE * secs)
    cycle = secs / 2  # one octave rise takes `cycle` seconds
    phases = [0.0] * octaves
    out = []
    for i in range(n):
        t = i / RATE
        total = 0.0
        for k in range(octaves):
            pos = (k + (t / cycle)) % octaves  # position in octaves above base, wrapping
            freq = base * 2 ** pos
            amp = math.exp(-((pos - octaves / 2) ** 2) / (2 * (octaves / 6) ** 2))
            phases[k] += 2 * math.pi * freq / RATE
            total += amp * math.sin(phases[k])
        out.append(int(3500 * total))
    return out


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "shepard_tone.wav"
    samples = shepard()
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", max(-32768, min(32767, s))) for s in samples))
    print("wrote", path, len(samples), "samples")
