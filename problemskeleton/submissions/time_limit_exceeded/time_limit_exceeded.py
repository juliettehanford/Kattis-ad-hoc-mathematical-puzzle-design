import sys

data = sys.stdin.read().strip().split()
n = int(data[0])

idx = 1
bad = []

for _ in range(n):
    s = data[idx]
    idx += 1

    ok = True
    # For each prefix length, copy substring and convert to int
    for i in range(1, len(s) + 1):
        prefix = s[:i]                  # copies substring -> O(L)
        val = int(prefix)               # parses substring -> O(L) big-int work for long prefixes
        m = ((i - 1) % 10) + 1
        if val % m != 0:                # runtime is suboptimal - O(n * L^2) due to repeated parsing of prefix
            ok = False
            break

    if not ok:
        bad.append(s)

if not bad:
    print("secure")
else:
    print("not secure")
    print("\n".join(bad))