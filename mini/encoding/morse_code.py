"""Morse code encoder/decoder (letters, digits, basic punctuation)."""
MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.",
    "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.",
    "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-",
    "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
    "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "!": "-.-.--",
}
REVERSE = {v: k for k, v in MORSE.items()}


def encode(text: str) -> str:
    """Letters separated by space, words by ' / '."""
    words = text.upper().split()
    return " / ".join(" ".join(MORSE[c] for c in w if c in MORSE) for w in words)


def decode(code: str) -> str:
    return " ".join("".join(REVERSE[s] for s in w.split()) for w in code.split(" / "))


if __name__ == "__main__":
    msg = "SOS Hello World 42"
    enc = encode(msg)
    assert decode(enc) == msg.upper()
    print(enc)
