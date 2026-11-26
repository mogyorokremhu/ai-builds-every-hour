"""Tiny INI parser: [sections], key = value, ; or # comments, with type coercion."""


def parse_ini(text: str) -> dict[str, dict[str, object]]:
    """Parse INI text into {section: {key: value}}; top-level keys go in ''."""
    data: dict[str, dict[str, object]] = {"": {}}
    section = ""
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line[0] in ";#":
            continue
        if line.startswith("["):
            if not line.endswith("]"):
                raise ValueError(f"line {n}: unterminated section header")
            section = line[1:-1].strip()
            data.setdefault(section, {})
        elif "=" in line:
            key, _, val = line.partition("=")
            data[section][key.strip()] = _coerce(val.strip())
        else:
            raise ValueError(f"line {n}: expected key = value")
    if not data[""]:
        del data[""]
    return data


def _coerce(v: str) -> object:
    if v.lower() in ("true", "yes", "on"):
        return True
    if v.lower() in ("false", "no", "off"):
        return False
    for typ in (int, float):
        try:
            return typ(v)
        except ValueError:
            pass
    return v.strip("\"'")


if __name__ == "__main__":
    sample = "name = demo\n[server]\nport = 8080\ndebug = yes\nratio=0.5\n; note\n[paths]\nroot = '/tmp'\n"
    result = parse_ini(sample)
    assert result["server"] == {"port": 8080, "debug": True, "ratio": 0.5}
    assert result["paths"]["root"] == "/tmp" and result[""]["name"] == "demo"
    print(result)
