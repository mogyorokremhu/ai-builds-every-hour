"""Beating: two close sine frequencies produce a slow amplitude wobble. Usage: python beating.py [f1] [beat_hz] [out.wav]"""
import math
import struct
import sys
import wave

RATE = 22050

if __name__ == "__main__":
    f1 = float(sys.argv[1]) if len(sys.argv) > 1 else 440.0
    beat = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
    path = sys.argv[3] if len(sys.argv) > 3 else "beating.wav"
    n = RATE * 4
    data = b"".join(
        struct.pack("<h", int(9000 * (math.sin(2 * math.pi * f1 * i / RATE) + math.sin(2 * math.pi * (f1 + beat) * i / RATE))))
        for i in range(n)
    )
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(data)
    print("wrote", path, f"beat every {1 / beat:.2f}s")
