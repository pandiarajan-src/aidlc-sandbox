# Test Results

Commands come from `unit-test-instructions.md` in `aidlc/spaces/default/intents/261114-temperature-converter/construction/code-generation/`; the plan is `code-generation-plan.md` and the files built are listed in `code-summary.md`.

## Build status

Success. There is no build step. Running the script directly works:

- `--c-to-f 100` printed `212.00`
- `--f-to-c 212` printed `100.00`
- `100 C` then `q` in interactive mode printed `212.00 F` and exited
- `--c-to-f abc` wrote `error: not a number: 'abc'` to standard error and exited with code 1
- `--help` printed both flags, the interactive-mode note and one example per direction

## Unit tests

Command (once; this is the stage-level command, identical for the whole project):

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest test_temp_convert.py -q -p no:cacheprovider
```

Result: exit code 0. Python 3.14.8, pytest 9.2.0.

| Total | Passed | Failed | Skipped |
|-------|--------|--------|---------|
| 40 | 40 | 0 | 0 |

## Failure details

None.

## Coverage

No coverage run. The `poc` scope adds no coverage floor and no coverage threshold is configured.

## Integration, performance and security checks

None generated: the Minimal test strategy generates no additional test instruction files, and there are no integration points, performance targets or security targets.

## Target Verification Matrix

See `build-and-test-summary.md`.

## Python 3.9 floor

The same test file was run on CPython 3.9.6 (the macOS system interpreter) in a temporary `uv` virtual environment with `pytest` 8.4.2: exit code 0, 40 passed, 0 failed, 0 skipped. The environment was removed afterwards.

## Not executed

- Python 3.10 to 3.13: not run. Only 3.9.6 and 3.14.8 were exercised.
