# Build Instructions

Inputs: `code-generation-plan.md`, `unit-test-instructions.md` and `code-summary.md` in `aidlc/spaces/default/intents/261114-celsius-sign-bug/construction/code-generation/`.

## Dependency installation

The converter uses only the Python standard library (NFR1), so there is nothing to install to run it. The tests need `pytest`. Per the project rule, install it with `uv` into a virtual environment:

```bash
uv venv .venv
uv pip install --python .venv/bin/python pytest
```

## Environment setup

- Python 3.9 or newer is the supported floor. This run used CPython 3.14.8 (`.venv`) and CPython 3.9.6 (a temporary `uv` environment).
- No environment variables, configuration files or local services.

## Build commands

None. The tool is a single script, `temp_convert.py`, with no compile, bundle or transpile step.

## Build verification

```bash
.venv/bin/python temp_convert.py --c-to-f -40     # prints -40.00
.venv/bin/python temp_convert.py --f-to-c -40     # prints -40.00
.venv/bin/python temp_convert.py --c-to-f -1e2    # prints -148.00
.venv/bin/python temp_convert.py --c-to-f -inf    # message on standard error, exit 1
```

Python 3.9 check, with a temporary virtual environment that is removed afterwards:

```bash
uv venv --python /usr/bin/python3 .venv-py39
uv pip install --python .venv-py39/bin/python pytest
.venv-py39/bin/python -m pytest test_temp_convert.py -q
rm -rf .venv-py39
```

## Troubleshooting

- `No module named pytest`: run the two `uv` commands under "Dependency installation", then call `.venv/bin/python -m pytest`, not the system `python`.
- A bad value such as `-inf` or `-abc` after `--c-to-f` exits with code 1 and a message from the converter. Bad flags (an unknown flag, both flags together) still exit with code 2.
