# Test Results

## Build status

Success. There is no build step; `temp_convert.py` runs as a script.

## Test results

| Run | Command | Total | Passed | Failed | Skipped | Exit code |
|---|---|---|---|---|---|---|
| CPython 3.14.8 (`.venv`) | `.venv/bin/python -m pytest test_temp_convert.py -q` | 58 | 58 | 0 | 0 | 0 |
| CPython 3.9.6 (temporary `uv` environment, pytest 8.4.2) | `.venv-py39/bin/python -m pytest test_temp_convert.py -q` | 58 | 58 | 0 | 0 | 0 |

The 58 are the original 40 plus 18 new cases from 7 new test functions. The commands come from `unit-test-instructions.md` in Code Generation; it is the only unit-test instructions file, so no command ran twice.

## Failure details

None.

## Coverage report

No coverage tool is configured and no coverage floor applies (the `bugfix` scope adds a targeted regression, not a coverage floor). Every requirement FR1.1 to FR2.3 has at least one passing test.

## Direct checks

| Command | Output | Exit code |
|---|---|---|
| `.venv/bin/python temp_convert.py --c-to-f -40` | `-40.00` | 0 |
| `.venv/bin/python temp_convert.py --f-to-c -40` | `-40.00` | 0 |
| `.venv/bin/python temp_convert.py --c-to-f -1e2` | `-148.00` | 0 |
| `.venv/bin/python temp_convert.py --c-to-f -inf` | `error: not a finite number: '-inf'` (standard error) | 1 |
| `.venv-py39/bin/python temp_convert.py --c-to-f -1e2` | `-148.00` | 0 |

On Python 3.9 this last command failed before the change (`argument --c-to-f: expected one argument`, exit 2), as recorded in `code-summary.md`.

## Import check

`ast` import scan of `temp_convert.py`: `['argparse', 'math', 're', 'sys']`, all standard library (`sys.stdlib_module_names`).

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| NFR1 | requirements.md > NFR1 | Standard library only; works on Python 3.9 or newer | Imports are `argparse`, `math`, `re`, `sys`; suite passes on CPython 3.9.6 | Import check above; 3.9.6 run above | build-and-test | Met |
| NFR2 | requirements.md > NFR2 | New tests use `pytest`, installed and run through `uv` in a virtual environment | `pytest` 9.2.0 in `.venv` and 8.4.2 in a temporary environment, both installed with `uv pip install` | Test results table above | build-and-test | Met |
| FR1 | requirements.md > FR1.1, FR1.2 | -40 gives `-40.00` through every way in; `-10` gives `14.00` and `-23.33` | All covered by passing tests; direct runs of `--c-to-f -40` and `--f-to-c -40` print `-40.00` | Test results and direct checks above | build-and-test | Met |
| FR2 | requirements.md > FR2.1, FR2.2, FR2.3 | `-1e2` gives `-148.00` without `=`; `-inf` is rejected with exit 1; the original 40 tests stay green | `-1e2` prints `-148.00` on 3.14 and 3.9; `-inf` exits 1; 40 original tests pass | Test results and direct checks above | build-and-test | Met |
