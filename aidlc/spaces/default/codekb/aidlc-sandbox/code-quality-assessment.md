# Code Quality Assessment

## Reported Defect: -40 C sign (celsius-sign-bug)
Not reproducible by reading the code (nothing was executed):
- `c_to_f(-40)` = `-40 * 9.0 / 5.0 + 32.0` = -72 + 32 = -40 (`temp_convert.py:35`).
- `f_to_c(-40)` = `(-40 - 32) * 5.0 / 9.0` = -40 (`temp_convert.py:40`).
- `format_result` only rewrites the exact text `-0.00` (`temp_convert.py:46-47`), so `-40.00` is untouched.
- Interactive regex `^(?P<value>.+?)\s*(?P<unit>[cCfF])$` keeps the `-` in the value group (`temp_convert.py:30`).
- One-shot `--c-to-f -40` is accepted by argparse as a negative-number argument, because the parser defines no option that looks like a negative number.

## Tests
- pytest, in `test_temp_convert.py`, covering the logic layer, one-shot and interactive CLI, bad input, negative-zero normalisation, and help text.
- -40 is asserted for `c_to_f`, `f_to_c`, `--c-to-f -40`, and `--f-to-c -40` (`test_temp_convert.py:21, 35, 44`).
- Gaps: interactive `-40 C`/`-40F`, `--c-to-f=-40`, decimal forms such as `-40.0`.
- Coverage config: absent.

## Tooling and Documentation
- Linting, formatting, CI/CD: none.
- Documentation: module docstring and `--help` epilog; no README.

## Technical Debt
- No dependency manifest or pinned versions.
- `_Parser` overrides the private `_print_message` argparse hook (`temp_convert.py:94`), which may break across Python versions.
