"""Pulse-width modulation: a square wave whose duty cycle sweeps 10%..90%. Usage: python square_pwm.py [out.wav]"""
import struct
import sys
import wave

RATE = 22050


def pwm(freq: float = 220.0, secs: float = 3.0) -> list[int]:
    out, phase, n = [], 0.0, int(RATE * secs)
    for i in range(n):
        duty = 0.1 + 0.8 * (0.5 + 0.5 * __import__("math").sin(2 * 3.14159 * 0.5 * i / RATE))
        phase = (phase + freq / RATE) % 1.0
        out.append(8000 if phase < duty else -8000)
    return out


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "square_pwm.wav"
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in pwm()))
    print("wrote", path)
