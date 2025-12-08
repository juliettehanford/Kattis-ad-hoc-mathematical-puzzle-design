#!/usr/bin/env python3

# This is a sample input validator, written in Python 3.

# Please refer to the comments in README.md for a description of the syntax it
# is validating. Then, change it as you need.

import sys
import re

n_line = sys.stdin.readline()
print(repr(n_line)) # useful for debugging to see where we have read
assert re.match('^[1-9][0-9]*\n$', n_line) # first line must be an integer with no leading zeros
n = int(n_line)
assert 1 <= n <= 5000 # n is positive, there are ≤1000 passcodes in the firewall

for _ in range(n):
    case_line = sys.stdin.readline()
    print(repr(case_line)) # useful for debugging to see where we have read

    # each passcode must be a positive integer, 1–25 digits, no leading zeros
    assert re.match('^[1-9][0-9]{0,99}\n$', case_line)

# ensure no extra input
assert sys.stdin.readline() == ''

# if we get here, all is well; use exit code 42.
sys.exit(42)

