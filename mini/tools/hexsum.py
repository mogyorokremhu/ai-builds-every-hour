#!/usr/bin/env python3
"""hexsum - checksums of files/stdin: CRC32, Adler-32, MD5, SHA-1, SHA-256 (`-a ALGO` picks one). `--selftest` runs checks."""
import hashlib
import sys
import zlib

def digests(data: bytes) -> dict:
    return {"crc32": f"{zlib.crc32(data):08x}", "adler32": f"{zlib.adler32(data):08x}",
            "md5": hashlib.md5(data).hexdigest(), "sha1": hashlib.sha1(data).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest()}

def main(argv):
    algo = None
    if "-a" in argv:
        i = argv.index("-a"); algo = argv[i + 1]; argv = argv[:i] + argv[i + 2:]
    sources = [(f, open(f, "rb").read()) for f in argv] or [("-", sys.stdin.buffer.read())]
    for name, data in sources:
        d = digests(data)
        if algo:
            print(f"{d[algo]}  {name}")
        else:
            for k, v in d.items():
                print(f"{k:>7}  {v}  {name}")

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        d = digests(b"abc")
        assert d["crc32"] == "352441c2" and d["adler32"] == "024d0127"
        assert d["md5"] == "900150983cd24fb0d6963f7d28e17f72"
        print("ok")
    else:
        main(sys.argv[1:])
