"""Stereo ping-pong: a tone that pans left to right and back. Usage: python stereo_pan.py [freq_hz] [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050


def pan_samples(freq: float, secs: float = 4.0, pan_hz: float = 0.5) -> list[tuple[int, int]]:
    out = []
    for i in range(int(RATE * secs)):
        t = i / RATE
        s = math.sin(2 * math.pi * freq * t) * 12000
        p = (math.sin(2 * math.pi * pan_hz * t) + 1) / 2  # 0 = left, 1 = right
        out.append((int(s * math.cos(p * math.pi / 2)), int(s * math.sin(p * math.pi / 2))))
    return out


if __name__ == "__main__":
    f = float(sys.argv[1]) if len(sys.argv) > 1 else 330.0
    path = sys.argv[2] if len(sys.argv) > 2 else "stereo_pan.wav"
    frames = pan_samples(f)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<hh", l, r) for l, r in frames))
    print("wrote", path, len(frames), "frames")
