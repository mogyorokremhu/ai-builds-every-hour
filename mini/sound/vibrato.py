"""Sine tone with vibrato (LFO-modulated pitch). Usage: python vibrato.py [freq_hz] [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050


def vibrato(freq: float, secs: float = 2.0, depth_hz: float = 6.0, lfo_hz: float = 5.0) -> list[int]:
    out, phase = [], 0.0
    for i in range(int(RATE * secs)):
        t = i / RATE
        f = freq + depth_hz * math.sin(2 * math.pi * lfo_hz * t)
        phase += 2 * math.pi * f / RATE
        out.append(int(12000 * math.sin(phase)))
    return out


if __name__ == "__main__":
    freq = float(sys.argv[1]) if len(sys.argv) > 1 else 440.0
    path = sys.argv[2] if len(sys.argv) > 2 else "vibrato.wav"
    s = vibrato(freq)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", x) for x in s))
    print("wrote", path, len(s), "samples")
