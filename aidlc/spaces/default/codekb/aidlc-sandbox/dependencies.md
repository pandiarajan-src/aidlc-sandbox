# Dependencies

## External
- Runtime: none beyond the Python standard library (see `technology-stack.md`).
- Test-only: `pytest`, unpinned; no manifest records it.

## Internal
- `test_temp_convert.py` imports `c_to_f`, `f_to_c`, `format_result`, `main`, `parse_finite` from `temp_convert`.
- No other cross-module dependencies.

No security advisories or version conflicts can be assessed: nothing is pinned.
