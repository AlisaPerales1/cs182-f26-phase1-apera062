import subprocess

tests = ["tiny.py", "test.py"]

total = len(tests)
passed = 0
failed = 0

for test in tests:
    try:
        subprocess.run(
            ["python", "Part1.py", test],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )

        passed += 1

    except Exception as e:
        print(f"[FAIL] {test}: {e}")
        failed += 1

print("==============================")
print(f"TOTAL: {total}")
print(f"PASSED: {passed}")
print(f"FAILED: {failed}")
print("==============================")
