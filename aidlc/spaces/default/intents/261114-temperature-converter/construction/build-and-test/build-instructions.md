# Build Instructions

Inputs: `code-generation-plan.md`, `unit-test-instructions.md` and `code-summary.md` in `aidlc/spaces/default/intents/261114-temperature-converter/construction/code-generation/`.

## Dependency installation

The converter uses only the Python standard library (NFR1), so there is nothing to install to run it. The tests need `pytest`. Per the project rule, install it with `uv` into a virtual environment:

```bash
uv venv .venv
uv pip install --python .venv/bin/python pytest
```

## Environment setup

- Python 3.9 or newer is the supported floor (requirements assumption). The build in this run used CPython 3.14.8.
- No environment variables, configuration files or local services.

## Build commands

None. The tool is a single Python script, `temp_convert.py`, with no compile, bundle or transpile step.

## Build verification

```bash
.venv/bin/python temp_convert.py --c-to-f 100    # prints 212.00
.venv/bin/python temp_convert.py --f-to-c 212    # prints 100.00
.venv/bin/python temp_convert.py --help          # exits 0
```

## Troubleshooting

- `No module named pytest`: run the two `uv` commands above, then call `.venv/bin/python -m pytest`, not the system `python`.
- `--c-to-f -1e5` fails with "expected one argument": write it as `--c-to-f=-1e5`. This is how `argparse` reads a leading-dash value that is not a plain number.
