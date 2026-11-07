"""Print a directory tree with sizes, like `tree -h` — plus a size summary.

    python tree.py [DIR] [-d DEPTH] [-a] [--sort size|name]

Hidden files and common junk folders (.git, __pycache__, node_modules) are skipped
unless -a is given.
"""
from __future__ import annotations

import argparse
import os

JUNK = {".git", "__pycache__", "node_modules", ".mypy_cache", ".pytest_cache", ".venv"}


def human(n: int) -> str:
    size = float(n)
    for unit in ("B", "K", "M", "G", "T"):
        if size < 1024 or unit == "T":
            return f"{size:.0f}{unit}" if unit == "B" else f"{size:.1f}{unit}"
        size /= 1024
    return f"{n}B"


def dir_size(path: str, show_all: bool) -> int:
    total = 0
    for root, dirs, files in os.walk(path):
        if not show_all:
            dirs[:] = [d for d in dirs if d not in JUNK and not d.startswith(".")]
        for f in files:
            try:
                total += os.lstat(os.path.join(root, f)).st_size
            except OSError:
                pass
    return total


def walk(path: str, prefix: str, depth: int, max_depth: int, show_all: bool, sort: str,
         stats: dict[str, int], out: list[str]) -> None:
    try:
        names = os.listdir(path)
    except OSError as exc:
        out.append(f"{prefix}└── [error: {exc.strerror}]")
        return
    if not show_all:
        names = [n for n in names if not n.startswith(".") and n not in JUNK]
    entries = []
    for n in names:
        full = os.path.join(path, n)
        is_dir = os.path.isdir(full) and not os.path.islink(full)
        size = dir_size(full, show_all) if is_dir else os.lstat(full).st_size
        entries.append((n, full, is_dir, size))
    if sort == "size":
        entries.sort(key=lambda e: -e[3])
    else:
        entries.sort(key=lambda e: (not e[2], e[0].lower()))
    for i, (n, full, is_dir, size) in enumerate(entries):
        last = i == len(entries) - 1
        branch = "└── " if last else "├── "
        label = n + ("/" if is_dir else "")
        out.append(f"{prefix}{branch}[{human(size):>6}] {label}")
        stats["dirs" if is_dir else "files"] += 1
        if is_dir and depth < max_depth:
            walk(full, prefix + ("    " if last else "│   "), depth + 1, max_depth, show_all, sort, stats, out)


def tree(path: str, max_depth: int = 99, show_all: bool = False, sort: str = "name") -> list[str]:
    stats = {"dirs": 0, "files": 0}
    out = [f"{path} [{human(dir_size(path, show_all))}]"]
    walk(path, "", 1, max_depth, show_all, sort, stats, out)
    out.append("")
    out.append(f"{stats['dirs']} directories, {stats['files']} files")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", nargs="?", default=".")
    ap.add_argument("-d", "--depth", type=int, default=99)
    ap.add_argument("-a", "--all", action="store_true")
    ap.add_argument("--sort", choices=("name", "size"), default="name")
    a = ap.parse_args()
    print("\n".join(tree(a.dir, a.depth, a.all, a.sort)))


if __name__ == "__main__":
    main()
