import coverage
import runpy
import sys
from pathlib import Path


def run_target(program_path, input_path):

    text = ""

    if input_path:
        text = Path(input_path).read_text().strip()

    old_argv = sys.argv[:]

    try:

        sys.argv = [program_path]

        if text:
            sys.argv.append(text)

        cov = coverage.Coverage()

        cov.start()

        runpy.run_path(
            program_path,
            run_name="__main__"
        )

        cov.stop()
        cov.save()

        return cov

    finally:
        sys.argv = old_argv


def print_coverage(program_path, cov):

    filename, executable, _, missing, _ = \
        cov.analysis2(program_path)

    missing = set(missing)
    executable = set(executable)

    with open(program_path) as f:
        lines = f.readlines()

    for num, line in enumerate(lines, start=1):

        line = line.rstrip()

        if num in executable:

            if num in missing:
                prefix = "# "
            else:
                prefix = "  "

        else:
            prefix = "# "

        print(
            f"{prefix}{num:>4}: {line}"
        )


if __name__ == "__main__":

    program = sys.argv[1]

    input_file = None

    if len(sys.argv) > 2:
        input_file = sys.argv[2]

    cov = run_target(
        program,
        input_file
    )

    print_coverage(
        program,
        cov
    )