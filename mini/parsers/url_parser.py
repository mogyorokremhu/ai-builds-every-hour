"""Hand-written URL parser (scheme, userinfo, host, port, path, query, fragment)
with percent-decoding, checked against urllib.parse."""
from urllib.parse import urlsplit, parse_qsl, unquote


def parse_url(url: str) -> dict:
    """Split a URL into components without regexes."""
    out = {"scheme": "", "user": None, "host": "", "port": None,
           "path": "", "query": "", "fragment": ""}
    rest = url
    if "#" in rest:
        rest, out["fragment"] = rest.split("#", 1)
    if "?" in rest:
        rest, out["query"] = rest.split("?", 1)
    i = rest.find(":")
    if i > 0 and rest[0].isalpha() and all(c.isalnum() or c in "+-." for c in rest[:i]):
        out["scheme"] = rest[:i].lower()
        rest = rest[i + 1:]
    if rest.startswith("//"):
        rest = rest[2:]
        j = rest.find("/")
        auth, rest = (rest, "") if j < 0 else (rest[:j], rest[j:])
        if "@" in auth:
            out["user"], auth = auth.rsplit("@", 1)
        if auth.startswith("["):
            k = auth.find("]")
            out["host"] = auth[1:k]
            auth = auth[k + 1:]
        elif ":" in auth:
            auth, _, p = auth.rpartition(":")
            out["host"] = auth
            auth = ":" + p
        else:
            out["host"], auth = auth, ""
        if auth.startswith(":") and auth[1:].isdigit():
            out["port"] = int(auth[1:])
    out["path"] = rest
    return out


def query_params(query: str) -> list[tuple[str, str]]:
    """Decode a query string into (key, value) pairs."""
    pairs = []
    for part in filter(None, query.split("&")):
        k, _, v = part.partition("=")
        pairs.append((unquote(k.replace("+", " ")), unquote(v.replace("+", " "))))
    return pairs


if __name__ == "__main__":
    for u in ["https://user:pw@example.com:8080/a/b?x=1&y=a%20b+c#frag",
              "http://[::1]:3000/",
              "mailto:bob@example.com",
              "/relative/path?q=1",
              "ftp://host"]:
        mine = parse_url(u)
        ref = urlsplit(u)
        assert mine["scheme"] == ref.scheme, u
        assert mine["host"] == (ref.hostname or ""), u
        assert mine["port"] == ref.port, u
        assert mine["path"] == ref.path, u
        assert mine["query"] == ref.query and mine["fragment"] == ref.fragment, u
        assert query_params(mine["query"]) == parse_qsl(ref.query), u
        print(u, "->", mine)
    print("url_parser: all checks passed")
