"""Write a WAV file with a sine/square/saw/triangle tone. Usage: python tones.py [freq] [seconds] [wave] [out.wav]"""
import math, struct, sys, wave

RATE = 22050


def sample(wave_name: str, phase: float) -> float:
    """Value in [-1, 1] for phase in [0, 1)."""
    if wave_name == "square":
        return 1.0 if phase < 0.5 else -1.0
    if wave_name == "saw":
        return 2 * phase - 1
    if wave_name == "triangle":
        return 4 * abs(phase - 0.5) - 1
    return math.sin(2 * math.pi * phase)


def tone(freq: float, seconds: float, wave_name: str = "sine", volume: float = 0.5) -> list[int]:
    n = int(RATE * seconds)
    out = []
    for i in range(n):
        env = min(1.0, i / 200, (n - i) / 200)  # tiny fade to avoid clicks
        out.append(int(32767 * volume * env * sample(wave_name, (freq * i / RATE) % 1.0)))
    return out


def write_wav(path: str, samples: list[int]) -> None:
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))


if __name__ == "__main__":
    f = float(sys.argv[1]) if len(sys.argv) > 1 else 440.0
    d = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    kind = sys.argv[3] if len(sys.argv) > 3 else "sine"
    path = sys.argv[4] if len(sys.argv) > 4 else "tone.wav"
    write_wav(path, tone(f, d, kind))
    print(f"wrote {path}: {f} Hz {kind} for {d}s")
