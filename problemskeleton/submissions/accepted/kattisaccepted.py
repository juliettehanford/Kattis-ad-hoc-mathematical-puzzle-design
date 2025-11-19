import sys

data = sys.stdin.read().strip().split()     #Read all at once for efficiency
n = int(data[0])

idx = 1
bad = []

for _ in range(n):
    s = data[idx]
    idx += 1                                # Use manual incrementation so on last (n-1) line, increment again for n'th line

    val = 0                                 # Initialize carry-forward value to 0
    ok = True
    for i, ch in enumerate(s, start=1):     # Use enumerate to generate a counter alongside the character for modulo operation
        val = val * 10 + int(ch)            # Use carry-forward logic instead of rebuilding the prefix every time using basic principle of base 10 numbers
        if val % i != 0:                    # Due to this logic, runtime of O(n * L) where L is length of string
            ok = False
            break

    if not ok:
        bad.append(s)

if not bad:
    print("Firewall is secure!")
else:
    print("Vulnerabilities detected:")
    print("\n".join(bad))