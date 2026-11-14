# Requirements

Upstream input: the code knowledge base for this repository at `aidlc/spaces/default/codekb/aidlc-sandbox/` (`business-overview.md`, `architecture.md`, `code-structure.md`), and the answers in `requirements-analysis-questions.md`.

## Intent Analysis

The request was a bugfix: "converting -40C returns the wrong sign". The code scan (`code-structure.md`, `architecture.md`) and a direct run of the converter found no sign defect. Converting -40 C gives `-40.00` in every way in: the one-shot flags (`--c-to-f -40`, `--c-to-f -40.0`, `--c-to-f=-40`, `--f-to-c -40`) and interactive mode (`-40 C`, `-40C`, `-40 f`). The person confirmed they see `-40.00 F` in interactive mode and think that is correct (Q1, Q2). -40 C and -40 F are the same temperature, so a result of -40.00 is right.

What the person wants from this work is therefore protection against a sign regression, plus forgiving handling of negative numbers on any path that turns out to be fragile (Q3).

## Functional Requirements

### FR1. Regression tests for negative values

- **FR1.1** The test suite includes tests that -40 converts to `-40.00` in both directions through every way in: `--c-to-f` and `--f-to-c` with the value as a separate argument, `--c-to-f=-40` with the value joined by `=`, interactive mode with `-40 C` and `-40 F` (and the forms `-40C`, `-40f`), and the functions `c_to_f` and `f_to_c`. Pass criterion: each of these tests exists and passes, and each fails if the sign of the result is flipped.
- **FR1.2** The test suite includes at least one other negative value in each direction, with a result whose sign differs from -40 (for example `--c-to-f -10` prints `14.00`, and `--f-to-c -10` prints `-23.33`). Pass criterion: those tests exist and pass.

### FR2. Negative numbers on the one-shot flags

- **FR2.1** A one-shot flag accepts a negative number written in any ordinary way without needing `=`, including exponent forms such as `-1e5` and decimals without a leading digit such as `-.5`. Pass criterion: `--c-to-f -1e2` prints `-148.00` and `--c-to-f -.5` prints `31.10`, each with exit code 0.
- **FR2.2** A negative value that is not a finite number is still rejected as bad input. Pass criterion: `--c-to-f -inf` prints a short message to standard error, prints nothing to standard output, and exits with a non-zero code.
- **FR2.3** Everything the current tool does for non-negative values, bad input, `--help` and interactive mode stays as it is. Pass criterion: the existing 40 tests still pass with no change to what they assert.

## Non-Functional Requirements

- **NFR1** The tool still depends only on the Python standard library and works on Python 3.9 or newer. Pass criterion: no new imports outside the standard library, and the suite passes on Python 3.9.
- **NFR2** The new tests use `pytest`, are installed and run through `uv` in a virtual environment (the project rule in `aidlc/spaces/default/memory/project.md`), and need no setup beyond that. Pass criterion: the documented `uv` commands run the whole suite.

## Constraints

- The change is limited to `temp_convert.py` and `test_temp_convert.py` (`code-structure.md`); nothing outside those two files changes.
- Python packages are installed only with `uv` into a virtual environment.

## Assumptions

- The reported wrong sign does not exist in this code: the person sees `-40.00 F` and thinks it is correct (Q1). The work does not change how -40 is converted.
- A reader who sees a different result is running a different copy or version of the tool. Rationale: no other path through this code gives a different answer for -40.

## Out of scope

- Changing any conversion formula, rounding, or output format for any value.
- New units, new flags, or packaging.
- Investigating copies of the tool outside this folder.

## Open questions

None.
