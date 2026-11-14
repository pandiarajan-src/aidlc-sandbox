# Unit Test Instructions

## Test framework setup

- Framework: `pytest` (NFR2). The tool itself uses only the Python standard library (NFR1).
- Prerequisite: Python 3.9 or newer and `pytest` installed (`python -m pip install pytest`).
- No configuration file is needed.

## How to run the tests

```bash
python -m pytest test_temp_convert.py -q
```

This command is scoped to the converter's own test file and is runnable as soon as the tests exist.

## Test scope (Minimal strategy)

One requirement-driven test per requirement group, about 9 tests (some parametrized): FR1.1, FR1.2, FR2.1, FR2.2, FR2.3, FR3.1, FR3.2, FR3.3, FR4.1.

## Expected coverage targets

The poc scope adds no coverage floor. No coverage threshold is set.

## Mocking and stubbing

None needed. The command-line layer takes its input and output streams as parameters, so tests pass `io.StringIO` objects and read the exit code returned by `main(...)`.

## Test data

Fixed reference pairs: 100 C = 212.00 F, 0 C = 32.00 F, -40 C = -40.00 F, 212 F = 100.00 C, 32 F = 0.00 C. The `-0.00` case uses `--c-to-f -17.7777778`, which prints `0.00`.
