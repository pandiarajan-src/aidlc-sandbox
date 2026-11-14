# Code Summary

## Files created

- `temp_convert.py`: the converter. Standard library only (NFR1). `c_to_f`, `f_to_c`, `format_result`, `parse_finite`, `main(argv, stdin, stdout, stderr)`.
- `test_temp_convert.py`: 40 `pytest` test cases covering FR1.1 to FR4.1 (parametrized).

No existing files were changed. `.gitignore` and `.mcp.json` are untouched.

## How to run

```bash
python temp_convert.py --c-to-f 100      # 212.00
python temp_convert.py --f-to-c 212      # 100.00
python temp_convert.py                   # interactive mode (q, Q, empty line or Ctrl-D to quit)
python temp_convert.py --help
```

Tests, using the virtual environment you asked for (created with `uv`, `pytest` installed there):

```bash
uv venv .venv
uv pip install --python .venv/bin/python pytest
.venv/bin/python -m pytest test_temp_convert.py -q
```

## Test results

`40 passed` with `pytest 9.2.0` on CPython 3.14.8 (the `.venv` interpreter).

## Key implementation decisions

- `main` takes its input and output streams as parameters and returns the exit code, so tests need no mocking.
- Argument errors (both flags, unknown flag, stray positional, missing value) come from `argparse`: message on standard error, exit code 2. Bad values and non-finite results exit with code 1.
- Interactive mode prints a `> ` prompt to standard output and a newline on end-of-input.

## Deviations from the plan

- The developer's first build had a skipped test case (`1e308` with `--f-to-c`, which converts to a finite value). I replaced the skip with an explicit list of error cases, so there are no skipped tests.
- `.venv/` was created in the project root at your request. `uv` put its own `.gitignore` inside it, so git does not list it; the project's `.gitignore` is untouched.
- After the review, at your request: values containing an underscore (such as `1_0`) are now rejected as bad input; tests were added for `1e999`, `1_0` and an exponent value (`--c-to-f=-1e2`); and the interactive exit test now checks that nothing after `q`, `Q` or an empty line is converted. Plan Step 8 covers this.
- After the second review, at your request: any value containing non-ASCII characters (such as Arabic-Indic digits) is rejected as bad input, with tests for the one-shot and interactive paths. Plan Step 9 covers this.

## Known limits

- A negative value written as `--c-to-f -1e5` or `--c-to-f -inf` is read by `argparse` as another flag, so it fails with "expected one argument" (exit 2). `--c-to-f=-1e5` works. This still gives a non-zero exit with a message on standard error. Plain negative numbers such as `-40` work.
- The minimum-version assumption (Python 3.9 or newer) was not tested here; Build and Test later ran the suite on Python 3.9.6 and it passed (`build-and-test/test-results.md`).

## Tests written but not executed

None.
