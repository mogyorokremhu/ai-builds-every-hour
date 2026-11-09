#!/usr/bin/env python3
"""Base64 encode/decode stdin: b64.py [-d] [--url]"""
import argparse, base64, sys
ap = argparse.ArgumentParser()
ap.add_argument("-d", action="store_true", help="decode")
ap.add_argument("--url", action="store_true", help="URL-safe alphabet")
a = ap.parse_args()
data = sys.stdin.buffer.read().strip() if a.d else sys.stdin.buffer.read()
enc, dec = (base64.urlsafe_b64encode, base64.urlsafe_b64decode) if a.url else (base64.b64encode, base64.b64decode)
out = dec(data) if a.d else enc(data)
sys.stdout.buffer.write(out + (b"" if a.d else b"\n"))
