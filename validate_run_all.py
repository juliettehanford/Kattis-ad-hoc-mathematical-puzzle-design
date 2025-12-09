#!/usr/bin/env python3
"""
Validate all .in files with the validator, then run accepted solution and compare outputs.

Usage:
    python3 tools/validate_and_run_all.py
"""
import subprocess
import sys
from pathlib import Path
import difflib

# Paths (adjust if your layout differs)
ROOT = Path.cwd()
VALIDATOR = ROOT / "problemskeleton" / "input_format_validators" / "validate.py"
ACCEPTED = ROOT / "problemskeleton" / "submissions" / "accepted" / "kattisaccepted.py"
SAMPLE_DIR = ROOT / "problemskeleton" / "data" / "sample"
SECRET_DIR = ROOT / "problemskeleton" / "data" / "secret"

if not VALIDATOR.exists():
    print(f"Validator not found: {VALIDATOR}", file=sys.stderr)
    sys.exit(2)
if not ACCEPTED.exists():
    print(f"Accepted solver not found: {ACCEPTED}", file=sys.stderr)
    sys.exit(2)

# gather .in files
in_files = sorted(SAMPLE_DIR.glob("*.in")) + sorted(SECRET_DIR.glob("*.in"))
if not in_files:
    print("No .in files found under sample/ or secret/", file=sys.stderr)
    sys.exit(2)

failures = []
total = 0

def run_validator(infile: Path):
    """
    Run validator with infile as stdin.
    Return (exit_code, stdout, stderr).
    """
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        stdin=infile.open("rb"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60
    )
    return proc.returncode, proc.stdout.decode(errors="replace"), proc.stderr.decode(errors="replace")

def run_accepted(infile: Path):
    """
    Run accepted solution with infile as stdin and capture stdout.
    """
    proc = subprocess.run(
        [sys.executable, str(ACCEPTED)],
        stdin=infile.open("rb"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=300  # increase if some tests are large
    )
    return proc.returncode, proc.stdout.decode(errors="replace"), proc.stderr.decode(errors="replace")

print(f"Found {len(in_files)} .in files. Validating + running accepted solver...\n")

for infile in in_files:
    total += 1
    ansfile = infile.with_suffix(".ans")
    print(f"--- {infile.relative_to(ROOT)} ---")

    # 1) validator
    code, out, err = run_validator(infile)
    # validator prints debugging repr lines in your current validator; ignore printed text but show status
    if code == 42:
        print("Validator: OK (exit 42)")
    else:
        print(f"Validator: FAIL (exit {code})")
        # show a short snippet of validator stdout/stderr for debugging
        if out:
            print("Validator stdout (snippet):")
            print("\n".join(out.splitlines()[:5]))
        if err:
            print("Validator stderr (snippet):")
            print("\n".join(err.splitlines()[:5]))
        failures.append((str(infile), "validator", code))
        # Even if validator fails, continue to run accepted solver so we can see what it would produce.
    # 2) run accepted solution
    code2, stdout2, stderr2 = run_accepted(infile)
    if stderr2:
        print("Accepted solver stderr (snippet):")
        print("\n".join(stderr2.splitlines()[:10]))
    if ansfile.exists():
        expected = ansfile.read_text()
        got = stdout2
        if expected.strip() == got.strip():
            print("Accepted output: OK (matches .ans)")
        else:
            print("Accepted output: MISMATCH with .ans")
            # show diff
            expected_lines = expected.splitlines()
            got_lines = got.splitlines()
            diff = difflib.unified_diff(
                expected_lines, got_lines,
                fromfile=str(ansfile), tofile=f"{infile}.out",
                lineterm=""
            )
            print("\n".join(list(diff)[:200]))  # print first 200 diff lines
            failures.append((str(infile), "mismatch", None))
    else:
        print("No .ans file to compare against. (Skipping comparison.)")
    print()

# summary
print("=== SUMMARY ===")
print(f"Total tests checked: {total}")
if failures:
    print(f"Failures: {len(failures)}")
    for f in failures:
        print(" -", f)
    sys.exit(1)
else:
    print("All tests passed validator+accepted-solver comparisons.")
    sys.exit(0)