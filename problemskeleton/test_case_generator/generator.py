#!/usr/bin/env python3
import os
import random

# ============================================================
#  Polydivisible Checker (matches accepted kattis solution)
# ============================================================
def is_polydivisible(s: str) -> bool:
    val = 0
    for i, ch in enumerate(s, start=1):
        val = val * 10 + int(ch)
        if val % i != 0:
            return False
    return True


def evaluate_firewall(codes):
    """Return judge-style output for list of codes."""
    bad = [s for s in codes if not is_polydivisible(s)]
    if not bad:
        return "secure\n"
    else:
        return "not secure\n" + "\n".join(bad) + "\n"


# ============================================================
#  Backtracking Generator for Polydivisible Numbers
# ============================================================
def generate_polydivisible_numbers(max_len=20, limit=5000):
    """
    Returns up to `limit` polydivisible numbers up to length `max_len`.
    Efficient via pruning.
    """
    results = []

    def backtrack(prefix_val, prefix_str, length):
        if len(results) >= limit:
            return

        if length > 0:
            results.append(prefix_str)

        if length == max_len:
            return

        start_digit = 1 if length == 0 else 0

        for d in range(start_digit, 10):
            new_val = prefix_val * 10 + d
            new_len = length + 1
            if new_val % new_len == 0:
                backtrack(new_val, prefix_str + str(d), new_len)

    backtrack(0, "", 0)
    return results


# Pre-generate secure passcodes
SECURE_POOL = generate_polydivisible_numbers(max_len=20, limit=5000)


# ============================================================
# Random Passcode Generation
# ============================================================
def random_passcode(min_len=1, max_len=20):
    length = random.randint(min_len, max_len)
    first = random.randint(1, 9)
    digits = [str(first)]
    for _ in range(length - 1):
        digits.append(str(random.randint(0, 9)))
    return "".join(digits)


def generate_insecure(min_len=1, max_len=20):
    """Generate a definitely-non-polydivisible number."""
    while True:
        s = random_passcode(min_len, max_len)
        if not is_polydivisible(s):
            return s


# ============================================================
# Case Generation Modes
# ============================================================
def make_case(num_codes, mode="mixed",
              min_len=1, max_len=20):
    """
    mode in {"mixed", "all_secure", "all_insecure"}
    """
    if mode == "all_secure":
        # direct sample from secure pool
        return random.sample(SECURE_POOL, num_codes)

    elif mode == "all_insecure":
        return [generate_insecure(min_len, max_len) for _ in range(num_codes)]

    elif mode == "mixed":
        out = []
        for _ in range(num_codes):
            if random.random() < 0.5:
                out.append(random.choice(SECURE_POOL))
            else:
                out.append(generate_insecure(min_len, max_len))
        return out

    else:
        raise ValueError(f"Unknown mode {mode}")


# ============================================================
# Helper to Write .in and .ans Files
# ============================================================
def write_case(base_path, name, codes):
    in_path = os.path.join(base_path, name + ".in")
    ans_path = os.path.join(base_path, name + ".ans")

    with open(in_path, "w") as f_in:
        f_in.write(str(len(codes)) + "\n")
        for s in codes:
            f_in.write(s + "\n")

    with open(ans_path, "w") as f_ans:
        f_ans.write(evaluate_firewall(codes))


# ============================================================
# Main Test-Set Generator
# ============================================================
def main():
    random.seed(123456)

    # Directory layout
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = os.path.join(root, "data")
    sample = os.path.join(data, "sample")
    secret = os.path.join(data, "secret")

    os.makedirs(sample, exist_ok=True)
    os.makedirs(secret, exist_ok=True)

    # --------------------------
    # Sample Test Cases (handmade)
    # Match problem statement samples exactly
    # --------------------------
    sample_cases = [
        ("sample1", ["381654729", "26", "58", "6"]),
        ("sample2", ["381654729", "6", "8"]),
        ("sample3", ["10", "12"]),
        ("sample4", ["38", "1", "123"]),
    ]
    for name, codes in sample_cases:
        write_case(sample, name, codes)

    # --------------------------
    # Secret Test Cases (20 total)
    # --------------------------
    secret_id = 1

    # Small random edge cases
    for n in [1, 2, 3]:
        write_case(secret, f"secret{secret_id}", make_case(n, "mixed"))
        secret_id += 1

    # Some all-secure using backtracking pool
    for n in [5, 10, 20]:
        write_case(secret, f"secret{secret_id}", make_case(n, "all_secure"))
        secret_id += 1

    # Some all-insecure
    for n in [10, 20]:
        write_case(secret, f"secret{secret_id}", make_case(n, "all_insecure"))
        secret_id += 1

    # Medium mixed
    for n in [50, 75, 100]:
        write_case(secret, f"secret{secret_id}", make_case(n, "mixed"))
        secret_id += 1

    # Large mixed (stress)
    for n in [200, 300, 500]:
        write_case(secret, f"secret{secret_id}", make_case(n, "mixed", min_len=10, max_len=20))
        secret_id += 1

    # Fill remaining up to secret20
    while secret_id <= 20:
        n = random.randint(50, 300)
        mode = random.choice(["mixed", "all_secure", "all_insecure"])
        write_case(secret, f"secret{secret_id}", make_case(n, mode))
        secret_id += 1


if __name__ == "__main__":
    main()