"""Build major, minor and modal scales from semitone step patterns."""
NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
MODES = {
    "ionian (major)": [2, 2, 1, 2, 2, 2, 1],
    "dorian": [2, 1, 2, 2, 2, 1, 2],
    "phrygian": [1, 2, 2, 2, 1, 2, 2],
    "lydian": [2, 2, 2, 1, 2, 2, 1],
    "mixolydian": [2, 2, 1, 2, 2, 1, 2],
    "aeolian (minor)": [2, 1, 2, 2, 1, 2, 2],
    "locrian": [1, 2, 2, 1, 2, 2, 2],
    "pentatonic minor": [3, 2, 2, 3, 2],
}


def scale(root: str, steps: list[int]) -> list[str]:
    """Return the note names of a scale starting on root."""
    i = NOTES.index(root)
    out = [NOTES[i]]
    for s in steps[:-1]:
        i = (i + s) % 12
        out.append(NOTES[i])
    return out


if __name__ == "__main__":
    for name, steps in MODES.items():
        print(f"C {name:18}", " ".join(scale("C", steps)))
    print("A natural minor:", " ".join(scale("A", MODES["aeolian (minor)"])))
