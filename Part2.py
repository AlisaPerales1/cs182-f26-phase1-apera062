import coverage
import runpy
import sys
from pathlib import Path


def run_target(program_path, input_path):
    text = ""
    if input_path and Path(input_path).exists():
        text = Path(input_path).read_text().strip()

    old_argv = sys.argv[:]
    try:
        sys.argv = [str(program_path)]
        if text:
            # Handle different input types
            parts = text.split()
            if len(parts) > 1:
                # Space-separated array
                sys.argv.extend(parts)
            else:
                sys.argv.append(text)

        cov = coverage.Coverage(branch=False, source=[str(Path(program_path).parent)])
        cov.start()
        try:
            runpy.run_path(str(program_path), run_name="__main__")
        except SystemExit:
            pass
        except Exception:
            pass
        cov.stop()
        return cov
    finally:
        sys.argv = old_argv


def print_coverage(program_path, cov):
    try:
        filename, executable, _, missing, _ = cov.analysis2(str(program_path))
    except Exception:
        # Fallback if analysis fails
        executable = set()
        missing = set()

    missing = set(missing)
    executable = set(executable)

    with open(program_path) as f:
        lines = f.readlines()

    for num, line in enumerate(lines, start=1):
        line = line.rstrip("\n")
        if num in executable:
            prefix = "# " if num in missing else "  "
        else:
            prefix = "# "
        print(f"{prefix}{num:>4}: {line}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Part2.py <program.py> [input.txt]")
        sys.exit(1)

    program = sys.argv[1]
    input_file = sys.argv[2] if len(sys.argv) > 2 else None

    cov = run_target(program, input_file)
    print_coverage(program, cov)
