"""White, brown and 'rain' noise to WAV files. Usage: python noise.py [white|brown|rain] [out.wav]"""
import random
import struct
import sys
import wave

RATE = 22050


def white(n: int) -> list[float]:
    return [random.uniform(-1, 1) for _ in range(n)]


def brown(n: int) -> list[float]:
    """Integrated white noise (random walk), clamped to [-1, 1]."""
    x, out = 0.0, []
    for _ in range(n):
        x = max(-1.0, min(1.0, x + random.uniform(-0.1, 0.1)))
        out.append(x)
    return out


def rain(n: int) -> list[float]:
    """White noise with random sparse droplet bursts."""
    out = [0.15 * s for s in white(n)]
    for _ in range(n // 800):
        p = random.randrange(n - 200)
        for k in range(200):
            out[p + k] += random.uniform(-1, 1) * 0.6 * (1 - k / 200)
    return [max(-1.0, min(1.0, s)) for s in out]


KINDS = {"white": white, "brown": brown, "rain": rain}

if __name__ == "__main__":
    kind = sys.argv[1] if len(sys.argv) > 1 else "rain"
    path = sys.argv[2] if len(sys.argv) > 2 else f"{kind}.wav"
    data = KINDS[kind](RATE * 3)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(s * 9000)) for s in data))
    print("wrote", path)
