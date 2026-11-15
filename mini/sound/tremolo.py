"""Tremolo: amplitude modulation of a chord by a slow LFO. Usage: python tremolo.py [rate_hz] [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050


def tremolo(rate_hz: float = 5.0, secs: float = 3.0) -> list[int]:
    out = []
    for i in range(int(RATE * secs)):
        t = i / RATE
        chord = sum(math.sin(2 * math.pi * f * t) for f in (261.63, 329.63, 392.0)) / 3
        lfo = 0.5 + 0.5 * math.sin(2 * math.pi * rate_hz * t)
        out.append(int(chord * lfo * 14000))
    return out


if __name__ == "__main__":
    rate = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0
    path = sys.argv[2] if len(sys.argv) > 2 else "tremolo.wav"
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in tremolo(rate)))
    print("wrote", path)
