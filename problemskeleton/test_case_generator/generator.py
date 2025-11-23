#!/usr/bin/env python3
import os
import random

# ============================================================
# CONSTANT: Longest-known base-10 polydivisible number
# ============================================================
FORCED = "3608528850368400786036725"   # 25 digits


# ============================================================
# Utility: Polydivisible Checker
# ============================================================
def is_polydivisible(s):
    val = 0
    for i, ch in enumerate(s, start=1):
        val = val * 10 + int(ch)
        if val % i != 0:
            return False
    return True


def evaluate_firewall(codes):
    bad = [s for s in codes if not is_polydivisible(s)]
    if not bad:
        return "secure\n"
    return "not secure\n" + "\n".join(bad) + "\n"


# ============================================================
# Insecure generators
# ============================================================
def random_passcode(min_len=2, max_len=30):
    """Random number, not guaranteed to be insecure."""
    L = random.randint(min_len, max_len)
    digits = [str(random.randint(1, 9))]
    digits += [str(random.randint(0, 9)) for _ in range(L - 1)]
    return "".join(digits)


def random_insecure(min_len=2, max_len=50):
    """Guaranteed to break polydivisibility early."""
    while True:
        s = random_passcode(min_len, max_len)
        if not is_polydivisible(s):
            return s


# ============================================================
# File output
# ============================================================
def write_case(base_path, name, codes):
    in_path = os.path.join(base_path, name + ".in")
    ans_path = os.path.join(base_path, name + ".ans")

    with open(in_path, "w") as f:
        f.write(str(len(codes)) + "\n")
        f.write("\n".join(codes) + "\n")

    with open(ans_path, "w") as f:
        f.write(evaluate_firewall(codes))


# ============================================================
# Main generator
# ============================================================
def main():
    random.seed(1234)

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = os.path.join(root, "data")
    sample = os.path.join(data, "sample")
    secret = os.path.join(data, "secret")
    os.makedirs(sample, exist_ok=True)
    os.makedirs(secret, exist_ok=True)

    # ---------------------------------------------------------
    # SAMPLE TESTS — unchanged from statement
    # ---------------------------------------------------------
    samples = [
        ("sample1", ["381654729", "26", "58", "6"]),
        ("sample2", ["381654729", "6", "8"]),
        ("sample3", ["10", "12"]),
        ("sample4", ["38", "1", "123"]),
    ]
    for name, codes in samples:
        write_case(sample, name, codes)

    # ---------------------------------------------------------
    # SECRET TESTS (exactly 20)
    # ---------------------------------------------------------
    sid = 1

    # 1. SINGLE FORCED (correctness)
    write_case(secret, f"secret{sid}", [FORCED])
    sid += 1

    # 2. SMALL MIXED WITH FORCED FIRST
    write_case(secret, f"secret{sid}",
                [FORCED, random_insecure(), random_insecure(), random_passcode()])
    sid += 1

    # 3–5. MEDIUM MIXED, FORCED FIRST
    for _ in range(3):
        codes = [FORCED] + [random_insecure() for _ in range(20)]
        write_case(secret, f"secret{sid}", codes)
        sid += 1

    # 6–8. BIG-N MIXED (n = 1000), FORCED FIRST
    for _ in range(3):
        codes = [FORCED] + [random_insecure(5, 50) for _ in range(999)]
        write_case(secret, f"secret{sid}", codes)
        sid += 1

    # 9. ALL-FORCED 1000 times
    codes = [FORCED] * 1000
    write_case(secret, f"secret{sid}", codes)
    sid += 1

    # 10. FORCED + EXTRA DIGIT (e.g., FORCED+"7") repeated 1000 times
    codes = [FORCED + str(random.randint(1, 9)) for _ in range(1000)]
    write_case(secret, f"secret{sid}", codes)
    sid += 1

    # 11–12. LONG NUMBER STRESS, FORCED FIRST
    # (random length ~2000)
    for _ in range(2):
        codes = [FORCED] + [
            random_insecure(500, 2000) for _ in range(10)
        ]
        write_case(secret, f"secret{sid}", codes)
        sid += 1

    # 13–15. MIXED WITH MULTIPLE FORCED INSERTIONS
    for _ in range(3):
        codes = []
        for i in range(40):
            if i % 7 == 0:
                codes.append(FORCED)
            else:
                codes.append(random_insecure())
        write_case(secret, f"secret{sid}", codes)
        sid += 1

    # 16–19. RANDOM MIXED (FORCED RANDOMLY INSERTED)
    for _ in range(4):
        codes = []
        n = random.randint(30, 60)
        forced_positions = random.sample(range(n), k=random.randint(3, 6))
        for i in range(n):
            if i in forced_positions:
                codes.append(FORCED)
            else:
                codes.append(random_insecure(2, 40))
        write_case(secret, f"secret{sid}", codes)
        sid += 1

    # 20. FINAL LARGE-N FULL MIX (forced first)
    codes = [FORCED] + [
        random_insecure(2, 40) for _ in range(999)
    ]
    write_case(secret, f"secret{sid}", codes)


if __name__ == "__main__":
    main()