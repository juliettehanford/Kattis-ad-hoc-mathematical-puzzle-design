import sys

data = sys.stdin.read().strip().split()     #Read all at once for efficiency
n = int(data[0])

idx = 1
bad = []

for _ in range(n):
    s = data[idx]
    idx += 1                                # Use manual incrementation so on last (n-1) line, increment again for n'th line

    ok = True
    for i, ch in enumerate(s, start=1):     
        if int(ch) % i != 0:                # Wrong Answer here is assuming that polydivisibility can be checked through individual numbers and ignoring base multiplication
            ok = False                      # ie. Checking number 1234 -> 1 % 1 = 0, 2 % 2 = 0, 3 % 3 = 0, 4 % 4 = 0 -> polydivisible (1234 is not polydivisible, since 1234 % 4 = 2)
            break

    if not ok:
        bad.append(s)

if not bad:
    print("Firewall is secure!")
else:
    print("Vulnerabilities detected:")
    print("\n".join(bad))