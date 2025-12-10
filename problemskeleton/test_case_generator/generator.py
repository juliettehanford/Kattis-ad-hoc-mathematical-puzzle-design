#!/usr/bin/env python3
import os
import random
from collections import deque

LCM_1_TO_10 = 2520

def m_k(k):
    return ((k - 1) % 10) + 1

# Functions based on ideal kattisaccepted.py
def is_cyclic_polydivisible(s):
    residual = 0
    for k, ch in enumerate(s, start=1):
        residual = (residual * 10 + int(ch)) % LCM_1_TO_10
        if residual % m_k(k) != 0:
            return False
    return True

def evaluate_firewall(codes):
    bad = [s for s in codes if not is_cyclic_polydivisible(s)]
    if not bad:
        return "secure\n"
    return "not secure\n" + "\n".join(bad) + "\n"


# Generate polydivisible numbers using backtracking search
def generate_polydivisible_numbers(max_len=900, limit=1000):
    results = []

    def backtrack(prefix_residual, prefix_str, length):
        if len(results) >= limit:
            return
        if length > 0:
            results.append(prefix_str)
        if length == max_len:
            return

        start_digit = 1 if length == 0 else 0
        for d in range(start_digit, 10):
            new_res = (prefix_residual * 10 + d) % LCM_1_TO_10
            new_len = length + 1
            if new_res % m_k(new_len) == 0:
                backtrack(new_res, prefix_str + str(d), new_len)
            # else skip this digit (it would break the cyclic rule at this prefix)

    backtrack(0, "", 0)
    return results

# Precompute library of cyclic-polydivisible numbers for sampling
POLYDIVISIBLE_NUMS = generate_polydivisible_numbers()


# Random passcode generation for stress-test
def random_passcode(min_len=1, max_len=4300):
    L = random.randint(min_len, max_len)
    digits = [str(random.randint(1, 9))]
    digits += [str(random.randint(0, 9)) for _ in range(L - 1)]
    return "".join(digits)

# Guaranteed incorrect passcode using random generation
def random_insecure(min_len=1, max_len=4300):
    while True:
        s = random_passcode(min_len, max_len)
        if not is_cyclic_polydivisible(s):
            return s


# Use backtracking search until fail point and then fill with random numbers for very large L sizes
def generate_near_polydivisible(target_len=4300):
    fail_point = random.randint(max(1, target_len // 2), max(1, target_len - 1))

    digits = []
    prefix_residual = 0

    for i in range(1, target_len + 1):
        if i < fail_point:
            found = False
            for d in range(0, 10):
                if i == 1 and d == 0:
                    continue
                cand_res = (prefix_residual * 10 + d) % LCM_1_TO_10
                if cand_res % m_k(i) == 0:
                    digits.append(str(d))
                    prefix_residual = cand_res
                    found = True
                    break
            if not found:
                # fallback: pick a digit and accept a temporary break
                d = random.randint(1 if i == 1 else 0, 9)
                digits.append(str(d))
                prefix_residual = (prefix_residual * 10 + d) % LCM_1_TO_10
        else:
            # after fail point, fill with random digits
            d = random.randint(0, 9)
            if i == 1 and d == 0:
                d = 1
            digits.append(str(d))
            prefix_residual = (prefix_residual * 10 + d) % LCM_1_TO_10

    return "".join(digits)


# Case creation using modes, standard = mixed, can also specify all insecure codes or all secure codes for specific testing criteria
def make_case(num_codes, mode="mixed"):
    if mode == "all_secure":
        if num_codes <= len(POLYDIVISIBLE_NUMS):
            return random.sample(POLYDIVISIBLE_NUMS, num_codes)
        else:
            # fallback: sample with replacement (guaranteed return)
            return [random.choice(POLYDIVISIBLE_NUMS) for _ in range(num_codes)]
    
    if mode == "all_insecure":
        return [random_insecure(1000, 4300) for _ in range(num_codes)]

    if mode == "mixed":
        out = []
        for _ in range(num_codes):
            r = random.random()
            if r < 0.3 and POLYDIVISIBLE_NUMS:
                out.append(random.choice(POLYDIVISIBLE_NUMS))
            elif r < 0.6:
                out.append(random_insecure(1000, 4300))
            else:
                out.append(generate_near_polydivisible(target_len=random.randint(1000, 4300)))
        return out

    raise ValueError("Unknown mode: " + mode)

# Function to write matching .in and .ans pairs into files
def write_case(base_path, name, codes):
    in_path = os.path.join(base_path, name + ".in")
    ans_path = os.path.join(base_path, name + ".ans")

    with open(in_path, "w") as f:
        f.write(str(len(codes)) + "\n")
        for s in codes:
            f.write(s + "\n")

    with open(ans_path, "w") as f:
        f.write(evaluate_firewall(codes))


def main():
    random.seed(1234)

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = os.path.join(root, "data")
    sample = os.path.join(data, "sample")
    secret = os.path.join(data, "secret")
    os.makedirs(sample, exist_ok=True)
    os.makedirs(secret, exist_ok=True)

    # Hard-coded sample tests from problem statement
    samples = [
        ("sample1", ["38165472", "4", "666450405060", "26"]),
        ("sample2", ["325","381654729", "63", "8"]),
        ("sample3", ["1", "38", "123"]),
    ]
    for name, codes in samples:
        write_case(sample, name, codes)

    # Secret tests
    sid = 1

    # 1 + 2. Small correctness tests
    for n in [1, 3]:
        write_case(secret, f"secret{sid}", make_case(n, "mixed"))
        sid += 1

    # 3 + 4. All-secure small/medium
    for n in [5, 20]:
        write_case(secret, f"secret{sid}", make_case(n, "all_secure"))
        sid += 1

    # 5. All-insecure medium
    write_case(secret, f"secret{sid}", make_case(10, "all_insecure"))
    sid += 1

    # 6 + 7. Near-polydivisible stress tests (long numbers, n=5)
    for _ in range(2):
        codes = [generate_near_polydivisible(target_len=random.randint(1000, 4300)) for _ in range(5)]
        write_case(secret, f"secret{sid}", codes)
        sid += 1

    # 8 - 11. Large n-tests for stress-testing performance
    write_case(secret, f"secret{sid}",
        [random.choice(POLYDIVISIBLE_NUMS) if random.random() < 0.3
         else random_insecure(5, 50)
         for _ in range(800)])
    sid += 1

    write_case(secret, f"secret{sid}",
        [random.choice(POLYDIVISIBLE_NUMS) if random.random() < 0.3
         else random_insecure(5, 50)
         for _ in range(1000)])
    sid += 1

    write_case(secret, f"secret{sid}", 
        [random_insecure(5, 50) for _ in range(1000)])
    sid += 1

    write_case(secret, f"secret{sid}",
        random.sample(POLYDIVISIBLE_NUMS, min(500, len(POLYDIVISIBLE_NUMS))))
    sid += 1

    # 12 + 13. Large mixed
    for _ in range(2):
        write_case(secret, f"secret{sid}",
            [random.choice(POLYDIVISIBLE_NUMS) if random.random() < 0.3
             else random_insecure(5, 50)
             for _ in range(1000)])
        sid += 1

    # 14 + 15. Mixed medium-sized tests
    for _ in range(2):
        write_case(secret, f"secret{sid}", make_case(40, "mixed"))
        sid += 1

    # 16 - 20. Mixed remaining tests
    while sid <= 20:
        write_case(secret, f"secret{sid}", make_case(random.randint(20, 40), "mixed"))
        sid += 1


if __name__ == "__main__":
    main()