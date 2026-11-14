# Component Inventory

## temp_convert.py
Single module; the components are listed below. Signatures are in `api-documentation.md`.

## Conversion functions
- Responsibility: arithmetic for C to F and F to C.
- Depends on: nothing.

## Formatting and parsing
- Responsibility: `format_result` (2-decimal text, no negative zero) and `parse_finite` (strict numeric input).
- Depends on: `math`.

## CLI driver
- Responsibility: `main`, `_build_parser`/`_Parser`, `_interactive`, `_convert`; argument handling, interactive loop, exit codes.
- Depends on: `argparse`, `re`, `sys`, `math`, and the components above.

## test_temp_convert.py
- Responsibility: pytest suite over the logic and CLI layers (see `code-quality-assessment.md`).
- Depends on: `temp_convert`, `pytest`.
