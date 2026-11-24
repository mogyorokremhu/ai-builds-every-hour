"""URL percent-encoding / decoding implemented by hand."""
import urllib.parse

SAFE = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")


def quote(s: str) -> str:
    return "".join(chr(b) if chr(b) in SAFE else f"%{b:02X}" for b in s.encode())


def unquote(s: str) -> str:
    out = bytearray()
    i = 0
    while i < len(s):
        if s[i] == "%" and len(s[i + 1:i + 3]) == 2:
            out.append(int(s[i + 1:i + 3], 16))
            i += 3
        else:
            out += s[i].encode()
            i += 1
    return out.decode()


if __name__ == "__main__":
    for t in ["a b&c=d/é", "100% ünï", "plain-text_ok~"]:
        assert quote(t) == urllib.parse.quote(t, safe="")
        assert unquote(quote(t)) == t
        print(t, "->", quote(t))
    print("percent ok")
