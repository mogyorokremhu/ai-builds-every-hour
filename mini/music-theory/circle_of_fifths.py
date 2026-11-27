"""Circle of fifths: key signatures, relative minors and neighbouring keys."""
SHARP_ORDER = ["F#", "C#", "G#", "D#", "A#", "E#", "B#"]
FLAT_ORDER = ["Bb", "Eb", "Ab", "Db", "Gb", "Cb", "Fb"]
MAJORS = ["C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"]
RELATIVE_MINOR = {"C": "Am", "G": "Em", "D": "Bm", "A": "F#m", "E": "C#m", "B": "G#m",
                  "F#": "D#m", "Db": "Bbm", "Ab": "Fm", "Eb": "Cm", "Bb": "Gm", "F": "Dm"}
SIGNATURE = {"C": 0, "G": 1, "D": 2, "A": 3, "E": 4, "B": 5, "F#": 6,
             "F": -1, "Bb": -2, "Eb": -3, "Ab": -4, "Db": -5}


def accidentals(key: str) -> list[str]:
    """Sharps or flats in a major key's signature."""
    n = SIGNATURE[key]
    return SHARP_ORDER[:n] if n >= 0 else FLAT_ORDER[:-n]


def neighbours(key: str) -> tuple[str, str]:
    """Dominant (up a fifth) and subdominant (down a fifth)."""
    i = MAJORS.index(key)
    return MAJORS[(i + 1) % 12], MAJORS[(i - 1) % 12]


if __name__ == "__main__":
    for k in MAJORS:
        dom, sub = neighbours(k)
        acc = " ".join(accidentals(k)) or "none"
        print(f"{k:3} rel {RELATIVE_MINOR[k]:4} IV={sub:3} V={dom:3} accidentals: {acc}")
