import sys

data = sys.stdin.read().strip().split()
n = int(data[0])

idx = 1
bad = []

for _ in range(n):
    s = data[idx]
    idx += 1

    val = 0
    ok = True
    for i, ch in enumerate(s, start=1):
        val = val * 10 + int(ch)
        if val % i != 0:
            ok = False
            break

    if not ok:
        bad.append(s)

if not bad:
    print("Firewall is secure!")
else:
    print("Vulnerabilities detected:")
    print("\n".join(bad))