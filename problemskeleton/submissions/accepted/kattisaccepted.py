'''
echo -e "1\n666450405060\n" | python3 problemskeleton/submissions/accepted/kattisaccepted.py
-> expect: secure

echo -e "1\n12345678910\n" | python3 problemskeleton/submissions/accepted/kattisaccepted.py
-> expect: not secure
'''

import sys

data = sys.stdin.read().strip().split()     # Read all at once for efficiency
n = int(data[0])

idx = 1
bad = []

for _ in range(n):
    s = data[idx]
    idx += 1            # Use manual incrementation so on last (n-1) line, increment again for n'th line
    
    # cyclic-polydivisible check using residual mod 2520 (LCM of 1..10)
    residual = 0
    ok = True
    for i, ch in enumerate(s, start=1):
        # update p_k % 2520 incrementally to avoid big integers
        residual = (residual * 10 + int(ch)) % 2520
        # cyclic modulus
        m = ((i - 1) % 10) + 1
        if residual % m != 0:
            ok = False
            break

    if not ok:
        bad.append(s)

if not bad:
    print("secure")
else:
    print("not secure")
    print("\n".join(bad))
    