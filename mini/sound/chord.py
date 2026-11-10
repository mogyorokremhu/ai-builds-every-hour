"""Mix chords into a WAV (major, minor, dominant 7th arpeggio then block). Usage: python chord.py [root_hz] [out.wav]"""
import sys
from tones import tone, write_wav

INTERVALS = {"major": [0, 4, 7], "minor": [0, 3, 7], "dom7": [0, 4, 7, 10]}


def chord(root: float, kind: str, seconds: float = 1.0) -> list[int]:
    """Sum the sine tones of a chord, scaled to avoid clipping."""
    voices = [tone(root * 2 ** (i / 12), seconds, "sine", 0.5) for i in INTERVALS[kind]]
    return [int(sum(v[i] for v in voices) / len(voices)) for i in range(len(voices[0]))]


if __name__ == "__main__":
    root = float(sys.argv[1]) if len(sys.argv) > 1 else 261.63
    path = sys.argv[2] if len(sys.argv) > 2 else "chords.wav"
    samples: list[int] = []
    for kind in INTERVALS:
        samples += chord(root, kind)
    write_wav(path, samples)
    print("wrote", path, "(major, minor, dom7)")
