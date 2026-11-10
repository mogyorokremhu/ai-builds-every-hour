#!/usr/bin/env python3
"""sumlines - sum/avg/min/max of the first number found on each input line (stdin or files). `--selftest` runs checks."""
import re
import sys

NUM = re.compile(r"-?\d+(?:,\d{3})*(?:\.\d+)?")

def numbers(lines):
    for l in lines:
        m = NUM.search(l)
        if m: yield float(m.group().replace(",", ""))

def summarize(nums):
    nums = list(nums)
    if not nums: return {}
    return {"count": len(nums), "sum": sum(nums), "avg": sum(nums) / len(nums), "min": min(nums), "max": max(nums)}

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        s = summarize(numbers(["a 1,000", "x -2.5 y", "none", "4"]))
        assert s["count"] == 3 and s["sum"] == 1001.5 and s["min"] == -2.5; print("ok"); sys.exit()
    files = [a for a in sys.argv[1:] if not a.startswith("-")]
    src = [l for f in files for l in open(f)] if files else sys.stdin
    for k, v in summarize(numbers(src)).items(): print(f"{k:>5}: {v:g}")
