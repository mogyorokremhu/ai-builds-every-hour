"""CIDR subnet calculator (stdlib only, no ipaddress module).

Usage: python cidr_calc.py [CIDR ...]   (no args runs a demo + self-check)
"""
import sys


def ip_to_int(ip: str) -> int:
    parts = [int(p) for p in ip.split(".")]
    if len(parts) != 4 or any(not 0 <= p <= 255 for p in parts):
        raise ValueError(f"bad IPv4 address: {ip}")
    return (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3]


def int_to_ip(n: int) -> str:
    return ".".join(str((n >> s) & 255) for s in (24, 16, 8, 0))


def describe(cidr: str) -> dict:
    """Return network, broadcast, mask, host range and host count."""
    ip, _, bits = cidr.partition("/")
    prefix = int(bits)
    if not 0 <= prefix <= 32:
        raise ValueError("prefix must be 0-32")
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    net = ip_to_int(ip) & mask
    bcast = net | (~mask & 0xFFFFFFFF)
    hosts = max(0, (1 << (32 - prefix)) - 2) if prefix < 31 else (1 << (32 - prefix))
    first, last = (net + 1, bcast - 1) if prefix < 31 else (net, bcast)
    return {"network": int_to_ip(net), "broadcast": int_to_ip(bcast),
            "mask": int_to_ip(mask), "first": int_to_ip(first),
            "last": int_to_ip(last), "hosts": hosts}


def main(args: list[str]) -> None:
    if args:
        for c in args:
            print(c, describe(c))
        return
    d = describe("192.168.10.77/26")
    assert d["network"] == "192.168.10.64" and d["broadcast"] == "192.168.10.127"
    assert d["mask"] == "255.255.255.192" and d["hosts"] == 62
    assert describe("10.0.0.1/31")["hosts"] == 2
    for c in ("192.168.10.77/26", "10.1.2.3/8", "172.16.5.4/20"):
        print(c, describe(c))
    print("ok")


if __name__ == "__main__":
    main(sys.argv[1:])
