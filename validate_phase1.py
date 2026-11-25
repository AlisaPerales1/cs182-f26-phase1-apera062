#!/usr/bin/env python3
"""
CS 182 Phase 1 validation script.
Runs all provided tests and compares outputs to expected results.
Reports TOTAL / PASSED / FAILED for each part.
"""
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent

# Paths relative to repo root (adjust if your layout differs)
PART1_SCRIPT = BASE / "Part1.py"
PART2_SCRIPT = BASE / "Part2.py"

PROGRAMS_DIR = BASE / "part1_program_cfg" / "programs"
EXPECTED_CFGS = BASE / "part1_program_cfg" / "expected_cfgs"

PART2_PROGRAMS = BASE / "part2_program_input_coverage" / "programs"
INPUTS_DIR = BASE / "part2_program_input_coverage" / "inputs"
EXPECTED_COV = BASE / "part2_program_input_coverage" / "expected_cov"

TIMEOUT_SEC = 60  # guidelines: limit to 1 minute

def run_cmd(cmd, timeout=TIMEOUT_SEC):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -1, "", str(e)

def files_match(actual_text, expected_path):
    """Simple line-by-line comparison after stripping trailing whitespace."""
    expected = expected_path.read_text()
    a = "\n".join(ln.rstrip() for ln in actual_text.splitlines())
    e = "\n".join(ln.rstrip() for ln in expected.splitlines())
    return a == e

def validate_part1():
    print("=" * 40)
    print("PART 1: CFG Generation")
    print("=" * 40)

    total = passed = failed = 0
    failures = []

    if not PART1_SCRIPT.exists():
        print("[ERROR] Part1.py not found")
        return 0, 0, 0

    for i in range(1, 11):
        prog_name = f"program_{i:02d}.py"
        prog = PROGRAMS_DIR / prog_name
        exp = EXPECTED_CFGS / f"program_{i:02d}_cfg.txt"

        if not prog.exists() or not exp.exists():
            print(f"[SKIP] {prog_name}: missing files")
            continue

        total += 1
        code, out, err = run_cmd([sys.executable, str(PART1_SCRIPT), str(prog)])

        if code == -1 and "timeout" in err:
            failed += 1
            failures.append(f"[FAIL] {prog_name}: timeout")
        elif code != 0:
            failed += 1
            reason = "error" if not err else err.splitlines()[0][:80]
            failures.append(f"[FAIL] {prog_name}: {reason}")
        elif files_match(out, exp):
            passed += 1
        else:
            failed += 1
            failures.append(f"[FAIL] {prog_name}: output mismatch")

    for f in failures:
        print(f)

    print("=" * 30)
    print(f"TOTAL: {total}")
    print(f"PASSED: {passed}")
    print(f"FAILED: {failed}")
    print("=" * 30)
    print()
    return total, passed, failed

def validate_part2():
    print("=" * 40)
    print("PART 2: Statement Coverage")
    print("=" * 40)

    total = passed = failed = 0
    failures = []

    if not PART2_SCRIPT.exists():
        print("[ERROR] Part2.py not found")
        return 0, 0, 0

    for i in range(1, 11):
        prog_name = f"program_{i:02d}.py"
        prog = PART2_PROGRAMS / prog_name
        cov_dir = EXPECTED_COV / f"program_{i:02d}"
        inp_dir = INPUTS_DIR / f"program_{i:02d}"

        if not prog.exists() or not cov_dir.exists():
            print(f"[SKIP] {prog_name}: missing files")
            continue

        # All 100 inputs
        for n in range(1, 101):
            inp_name = f"input_{n:03d}.txt"
            cov_name = f"input_{n:03d}_cov.txt"
            inp = inp_dir / inp_name
            exp = cov_dir / cov_name

            if not inp.exists() or not exp.exists():
                continue

            total += 1
            code, out, err = run_cmd(
                [sys.executable, str(PART2_SCRIPT), str(prog), str(inp)],
                timeout=TIMEOUT_SEC
            )

            if code == -1 and "timeout" in err:
                failed += 1
                failures.append(f"[FAIL] {prog_name} / {inp_name}: timeout")
            elif code != 0:
                failed += 1
                failures.append(f"[FAIL] {prog_name} / {inp_name}: error")
            elif files_match(out, exp):
                passed += 1
            else:
                failed += 1
                failures.append(f"[FAIL] {prog_name} / {inp_name}: output mismatch")

    # Print failures (limit to first 50 to avoid huge logs)
    for f in failures[:50]:
        print(f)
    if len(failures) > 50:
        print(f"... and {len(failures) - 50} more failures")

    print("=" * 30)
    print(f"TOTAL: {total}")
    print(f"PASSED: {passed}")
    print(f"FAILED: {failed}")
    print("=" * 30)
    print()
    return total, passed, failed

def main():
    print("CS 182 Phase 1 Validation")
    print()

    t1, p1, f1 = validate_part1()
    t2, p2, f2 = validate_part2()

    print("=" * 40)
    print("OVERALL")
    print(f"Part 1: {p1}/{t1} passed")
    print(f"Part 2: {p2}/{t2} passed")
    print("=" * 40)

if __name__ == "__main__":
    main()
