import sys

data = sys.stdin.read().strip().split()
n = int(data[0])

idx = 1
bad = []

for _ in range(n):
    s = data[idx]
    idx += 1

    ok = True
    for i in range(1, len(s) + 1):
        prefix = s[:i]              # Copies substring
        val = int(prefix)           # Parses substring and converts to int
        if val % i != 0:            # runtime is suboptimal - O(n * L^2) due to repeated parsing of prefix
            ok = False
            break

    if not ok:
        bad.append(s)

if not bad:
    print("secure")
else:
    print("not secure")
    print("\n".join(bad))