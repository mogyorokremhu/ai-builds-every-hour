"""Pretty-print, minify or sort JSON from a file or stdin.
Usage: jsonfmt.py [-m|--min] [-s|--sort] [file] | --selftest"""
import json
import sys


def fmt(text: str, minify: bool = False, sort: bool = False) -> str:
    data = json.loads(text)
    if minify:
        return json.dumps(data, separators=(",", ":"), sort_keys=sort, ensure_ascii=False)
    return json.dumps(data, indent=2, sort_keys=sort, ensure_ascii=False)


def selftest() -> None:
    assert fmt('{"b": 1,  "a": [1, 2]}', minify=True) == '{"b":1,"a":[1,2]}'
    assert fmt('{"b":1,"a":2}', minify=True, sort=True) == '{"a":2,"b":1}'
    assert fmt("[1]").splitlines() == ["[", "  1", "]"]
    print("jsonfmt ok")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--selftest"]:
        selftest()
        sys.exit()
    mini = "-m" in args or "--min" in args
    srt = "-s" in args or "--sort" in args
    files = [a for a in args if not a.startswith("-")]
    src = open(files[0]).read() if files else sys.stdin.read()
    try:
        print(fmt(src, mini, srt))
    except json.JSONDecodeError as e:
        sys.exit(f"invalid JSON: {e}")
