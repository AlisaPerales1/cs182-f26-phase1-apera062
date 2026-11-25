#!/usr/bin/env python3
"""
Validate Phase 1: compare student Part1 (CFG) and Part2 (coverage)
output against expected results.
"""
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent
# Adjust these paths if your repo layout differs
PROGRAMS_DIR = BASE / "part1_program_cfg" / "programs"
EXPECTED_CFGS = BASE / "part1_program_cfg" / "expected_cfgs"
PART2_PROGRAMS = BASE / "part2_program_input_coverage" / "programs"
INPUTS_DIR = BASE / "part2_program_input_coverage" / "inputs"
EXPECTED_COV = BASE / "part2_program_input_coverage" / "expected_cov"

PART1_SCRIPT = BASE / "Part1.py"
PART2_SCRIPT = BASE / "Part2.py"

def run_cmd(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)

def normalize(text):
    """Normalize whitespace for comparison."""
    lines = [ln.rstrip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln.strip())

def compare_outputs(actual, expected, label):
    a = normalize(actual)
    e = normalize(expected)
    if a == e:
        return True, "MATCH"
    # Simple diff summary
    a_lines = set(a.splitlines())
    e_lines = set(e.splitlines())
    missing = len(e_lines - a_lines)
    extra = len(a_lines - e_lines)
    return False, f"DIFF (missing={missing}, extra={extra})"

def main():
    total = 0
    passed = 0
    failed = 0
    results = []

    # ---- Part 1: CFG comparison ----
    print("=" * 50)
    print("PART 1: CFG Generation Comparison")
    print("=" * 50)

    if not PART1_SCRIPT.exists():
        print("[ERROR] Part1.py not found")
        sys.exit(1)

    for i in range(1, 11):
        prog = PROGRAMS_DIR / f"program_{i:02d}.py"
        exp_cfg = EXPECTED_CFGS / f"program_{i:02d}_cfg.txt"
        if not prog.exists() or not exp_cfg.exists():
            print(f"[SKIP] program_{i:02d}: missing files")
            continue

        total += 1
        code, out, err = run_cmd([sys.executable, str(PART1_SCRIPT), str(prog)])
        expected = exp_cfg.read_text()

        if code != 0:
            failed += 1
            msg = f"ERROR (exit={code})"
            print(f"[FAIL] program_{i:02d}: {msg}")
            if err:
                print(f"  stderr: {err[:200]}")
        else:
            ok, msg = compare_outputs(out, expected, f"program_{i:02d}")
            if ok:
                passed += 1
                print(f"[PASS] program_{i:02d}: {msg}")
            else:
                failed += 1
                print(f"[FAIL] program_{i:02d}: {msg}")

    # ---- Part 2: Coverage comparison (sample of inputs) ----
    print()
    print("=" * 50)
    print("PART 2: Coverage Comparison (first 5 inputs per program)")
    print("=" * 50)

    if not PART2_SCRIPT.exists():
        print("[ERROR] Part2.py not found")
        # Still report Part1 stats
    else:
        for i in range(1, 11):
            prog = PART2_PROGRAMS / f"program_{i:02d}.py"
            cov_dir = EXPECTED_COV / f"program_{i:02d}"
            inp_dir = INPUTS_DIR / f"program_{i:02d}"
            if not prog.exists() or not cov_dir.exists():
                print(f"[SKIP] program_{i:02d}: missing files")
                continue

            # Test first 5 inputs to keep CI time reasonable
            for n in range(1, 6):
                inp = inp_dir / f"input_{n:03d}.txt"
                exp = cov_dir / f"input_{n:03d}_cov.txt"
                if not inp.exists() or not exp.exists():
                    continue

                total += 1
                code, out, err = run_cmd(
                    [sys.executable, str(PART2_SCRIPT), str(prog), str(inp)],
                    timeout=20
                )
                expected = exp.read_text()

                if code != 0:
                    failed += 1
                    print(f"[FAIL] program_{i:02d}/input_{n:03d}: ERROR (exit={code})")
                else:
                    ok, msg = compare_outputs(out, expected, f"p{i}/i{n}")
                    if ok:
                        passed += 1
                        print(f"[PASS] program_{i:02d}/input_{n:03d}: {msg}")
                    else:
                        failed += 1
                        print(f"[FAIL] program_{i:02d}/input_{n:03d}: {msg}")

    # ---- Final statistics ----
    print()
    print("=" * 50)
    print("COMPARISON RESULTS AND STATISTICS")
    print("=" * 50)
    print(f"TOTAL:  {total}")
    print(f"PASSED: {passed}")
    print(f"FAILED: {failed}")
    if total > 0:
        print(f"PASS RATE: {100.0 * passed / total:.1f}%")
    print("=" * 50)

    # Exit non-zero if any failures (optional; comment out if you want CI green)
    # sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
