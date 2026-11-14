# Code Summary

## Files created and modified

- `temp_convert.py` (modified): added the helper `_join_negative_values(argv)` and one call to it in `main`, before `parse_args`. Nothing else in the file changed.
- `test_temp_convert.py` (modified): 7 new test functions (18 test cases) added at the end. The existing 40 tests are unchanged.
- No files were created. `.gitignore`, `OUTCOMES.md` and `.mcp.json` are untouched.

## Closing note for the original report

Converting -40 C gives `-40.00 F`, and -40 F gives `-40.00 C`, because the two scales meet at -40. The sign is correct, and the code did not have a sign defect in any way in. The tests below keep it that way.

## Observed before the change (plan Step 3)

Each command was `<python> temp_convert.py --c-to-f <value>`.

| Value | `.venv` (CPython 3.14.8) | `/usr/bin/python3` (CPython 3.9.6) |
|---|---|---|
| `-1e2` | `-148.00`, exit 0 | `temp_convert.py: error: argument --c-to-f: expected one argument`, exit 2 |
| `-.5` | `31.10`, exit 0 | `31.10`, exit 0 |
| `-inf` | `temp_convert.py: error: argument --c-to-f: expected one argument`, exit 2 | same message, exit 2 |
| `-40` | `-40.00`, exit 0 | `-40.00`, exit 0 |

So `-1e2` was a real failure on Python 3.9 only, and `-inf` was refused by `argparse` rather than by the converter on both. The helper makes every one of them reach `parse_finite`.

## Key implementation decisions

- `_join_negative_values` joins `--c-to-f` or `--f-to-c` with a following token that starts with a single `-` into `--flag=<token>`. It leaves `--...` tokens and `-h` alone, so unknown flags and help behave as before.
- Bad negative values (`-inf`, `-nan`, a bare `-`, `-1_0`, `-abc`) now fail with the converter's own message on standard error, no output on standard output, and exit code 1. Before, `-inf` exited 2 with an `argparse` message. Exit code 2 is still used for bad flags.
- The `--help` text and the module docstring are still correct, so they were left alone.

## New tests

| Requirement | Test |
|---|---|
| FR1.1 | `test_minus_40_both_directions`, `test_minus_40_equals_form`, `test_minus_40_interactive`, `test_minus_40_functions` |
| FR1.2 | `test_other_negative_values` |
| FR2.1 | `test_negative_exponent_and_decimal_forms` |
| FR2.2 | `test_negative_non_finite_rejected` |

Each test asserts the exact printed text.

## Test results

- `.venv` (CPython 3.14.8, pytest in a `uv` virtual environment): `58 passed`, 0 failed, 0 skipped. That is the original 40 plus 18 new cases.
- CPython 3.9.6 in a temporary `uv` virtual environment (removed afterwards): `58 passed`, 0 failed, 0 skipped.
- I re-ran the suite on `.venv` after the build and it printed `58 passed`.

## Deviations from the plan

- The developer wrote the new tests and ticked the plan boxes with shell commands (`cat >>` and `sed -i`) where the brief asked for file tools. The content is as planned; `git diff` shows exactly the changes listed above.

## Known limits

- Only CPython 3.9.6 and 3.14.8 were run, not 3.10 to 3.13.

## Tests written but not executed

None.
