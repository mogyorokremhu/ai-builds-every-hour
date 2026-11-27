"""Build triads and seventh chords from interval formulas and name chords from notes."""
NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
CHORDS = {
    "": (0, 4, 7), "m": (0, 3, 7), "dim": (0, 3, 6), "aug": (0, 4, 8),
    "sus4": (0, 5, 7), "7": (0, 4, 7, 10), "maj7": (0, 4, 7, 11), "m7": (0, 3, 7, 10),
}


def chord(root: str, kind: str = "") -> list[str]:
    """Notes of root+kind, e.g. chord('C', 'm7')."""
    r = NOTES.index(root)
    return [NOTES[(r + i) % 12] for i in CHORDS[kind]]


def identify(notes: list[str]) -> list[str]:
    """Return every chord name whose pitch-class set equals the given notes."""
    want = {NOTES.index(n) for n in notes}
    found = []
    for root in NOTES:
        for kind in CHORDS:
            if {NOTES.index(n) for n in chord(root, kind)} == want:
                found.append(root + kind)
    return found


if __name__ == "__main__":
    for r, k in [("C", ""), ("A", "m"), ("G", "7"), ("F", "maj7"), ("B", "dim")]:
        print(f"{r}{k:5}", " ".join(chord(r, k)))
    print("C E G# ->", identify(["C", "E", "G#"]))
    print("A C E G ->", identify(["A", "C", "E", "G"]))
