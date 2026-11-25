# CS 182 Phase 1

## Structure
- `Part1.py` — generates CFG information using py2cfg
- `Part2.py` — prints statement coverage using the coverage library
- `part1_program_cfg/` — example programs and expected CFG outputs
- `part2_program_input_coverage/` — example programs, inputs, and expected coverage
- `validate_phase1.py` — runs all tests and reports comparison statistics
- `.github/workflows/validate.yml` — GitHub Actions workflow

## How to run
```bash
pip install py2cfg coverage
python Part1.py path/to/program.py
python Part2.py path/to/program.py path/to/input.txt
python validate_phase1.py   # runs all provided tests and prints statistics
```

## GitHub Actions
On every push the workflow installs dependencies and runs `validate_phase1.py`, which compares outputs against the expected files and reports TOTAL / PASSED / FAILED for each part.
