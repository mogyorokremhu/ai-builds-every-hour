"""Supersaw: seven slightly detuned saw waves summed into a thick chord tone. Usage: python detune_supersaw.py [out.wav]"""
import struct
import sys
import wave

RATE = 22050
DETUNE_CENTS = (-14, -8, -3, 0, 3, 8, 14)


def supersaw(freq: float = 220.0, secs: float = 3.0) -> list[int]:
    out = []
    freqs = [freq * 2 ** (c / 1200) for c in DETUNE_CENTS]
    for i in range(int(RATE * secs)):
        t = i / RATE
        s = sum(2 * ((t * f) % 1.0) - 1 for f in freqs) / len(freqs)
        env = min(1.0, t / 0.05) * min(1.0, (secs - t) / 0.3)
        out.append(int(s * env * 14000))
    return out


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "detune_supersaw.wav"
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in supersaw()))
    print("wrote", path)
