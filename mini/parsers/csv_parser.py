"""CSV state-machine parser: quoted fields, escaped quotes (""), embedded newlines."""
import csv
import io


def parse_csv(text: str) -> list[list[str]]:
    rows, row, field = [], [], []
    in_q = False
    i = 0
    while i < len(text):
        c = text[i]
        if in_q:
            if c == '"':
                if text[i + 1:i + 2] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_q = False
            else:
                field.append(c)
        elif c == '"':
            in_q = True
        elif c == ",":
            row.append("".join(field))
            field = []
        elif c in "\r\n":
            if c == "\r" and text[i + 1:i + 2] == "\n":
                i += 1
            row.append("".join(field))
            rows.append(row)
            row, field = [], []
        else:
            field.append(c)
        i += 1
    if field or row:
        row.append("".join(field))
        rows.append(row)
    return rows


if __name__ == "__main__":
    data = 'name,quote\nAda,"Hello, ""world"""\nBob,"two\nlines"\n'
    for r in parse_csv(data):
        print(r)
    assert parse_csv(data) == list(csv.reader(io.StringIO(data, newline="")))
    print("matches csv.reader")
