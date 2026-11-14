# Unit Test Instructions

Based on `code-generation-plan.md` and `requirements.md` (FR1, FR2, NFR1, NFR2).

## Test framework setup

- Runner: `pytest`, already installed in the project's `uv` virtual environment at `.venv`.
- If `.venv` is missing, create it with `uv` (the project rule allows only `uv` and a virtual environment for Python tools):

```bash
uv venv .venv
uv pip install --python .venv/bin/python pytest
```

No configuration file is needed.

## How to run this work's tests

```bash
.venv/bin/python -m pytest test_temp_convert.py -q
```

Expected result: the existing 40 tests plus the new ones all pass, with 0 failed and 0 skipped.

Python 3.9 check (NFR1), using a temporary virtual environment that is removed afterwards:

```bash
uv venv --python /usr/bin/python3 .venv-py39
uv pip install --python .venv-py39/bin/python pytest
.venv-py39/bin/python -m pytest test_temp_convert.py -q
```

## Expected coverage targets

No coverage floor applies: the `bugfix` scope adds a targeted regression and requires the existing suite to stay green, and no threshold is configured. Every requirement FR1.1 to FR2.3 has at least one test.

## Mocking and stubbing

None. Tests call `main(argv, stdin, stdout, stderr)` with in-memory streams (`io.StringIO`) and read the exit code it returns.

## Test data

Inline values only: `-40`, `-10`, `-1e2`, `-.5`, `-inf`, `-nan`, and the interactive inputs `-40 C`, `-40C`, `-40 F`, `-40f`.
