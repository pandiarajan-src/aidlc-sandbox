# Requirements

Upstream input: `aidlc/spaces/default/intents/261114-temperature-converter/ideation/intent-capture/intent-statement.md` (intent-statement).

## Intent Analysis

Build a small Python command-line tool that converts temperatures between Celsius and Fahrenheit, with unit tests, as a proof of concept (intent-statement). The proof of concept must show both that the converter is correct and that the AI-DLC workflow can take a small idea through to tested code (intent-statement, Q1 of the intent questions). Other people will run the tool, so it needs clear usage help (intent-statement).

## Functional Requirements

### FR1. One-shot conversion

- **FR1.1** Given the flag `--c-to-f <number>`, the tool prints the Fahrenheit equivalent of that Celsius value, rounded to 2 decimal places, and exits with code 0. Pass criterion: `--c-to-f 100` prints `212.00`; `--c-to-f 0` prints `32.00`; `--c-to-f -40` prints `-40.00`.
- **FR1.2** Given the flag `--f-to-c <number>`, the tool prints the Celsius equivalent of that Fahrenheit value, rounded to 2 decimal places, and exits with code 0. Pass criterion: `--f-to-c 212` prints `100.00`; `--f-to-c 32` prints `0.00`; `--f-to-c -40` prints `-40.00`.

### FR2. Interactive mode

- **FR2.1** When started with no arguments, the tool repeatedly prompts for a value and unit written like `100 C` or `212 F`, prints the converted value in the other unit rounded to 2 decimal places, and prompts again. The unit is case-insensitive and the space between value and unit is optional. Pass criterion: input `100 C`, `100 c` and `100C` each print `212.00`; input `212 F` prints `100.00`.
- **FR2.2** The interactive mode exits with code 0 when the person enters `q` or `Q`, an empty line, or end-of-input (Ctrl-D). Pass criterion: each of `q`, `Q`, an empty line and end-of-input ends the session with exit code 0 and no traceback.
- **FR2.3** In interactive mode, an input that is not a finite number followed by `C` or `F` prints a short message to standard error and prompts again instead of ending the session.

### FR3. Bad input

- **FR3.1** When a one-shot flag receives a value that is not a finite number (text, `nan`, `inf`, `-inf` or a value too large to convert such as `1e999`), the tool prints a short message to standard error, prints nothing to standard output, and exits with a non-zero code. A conversion whose result is not finite (for example `--c-to-f 1e308`, which overflows to infinity) is treated the same way. Pass criterion: `--c-to-f abc`, `--c-to-f nan`, `--c-to-f inf` and `--c-to-f 1e308` each exit non-zero with a message on standard error.
- **FR3.2** When both one-shot flags are given together, an unknown flag is given, or a stray positional argument is given, the tool prints a short message to standard error, prints nothing to standard output, and exits with a non-zero code. Pass criterion: `--c-to-f 1 --f-to-c 1`, `--bogus` and `100` each exit non-zero with a message on standard error.
- **FR3.3** A result that rounds to zero is printed as `0.00`, never `-0.00`. Pass criterion: `--f-to-c 32` and `--c-to-f -17.7777778` print `0.00` rather than `-0.00`.

### FR4. Usage help

- **FR4.1** `--help` prints the invocation syntax for both one-shot flags, a note that running with no arguments starts interactive mode, and one worked example for each direction. `--help` exits with code 0. Pass criterion: the help text contains `--c-to-f`, `--f-to-c`, the interactive-mode note and two examples, and the exit code is 0.

## Non-Functional Requirements

- **NFR1** The tool depends only on the Python standard library. Pass criterion: running the tool requires no package installs.
- **NFR2** The unit tests use `pytest` and cover the pass criteria of FR1 to FR4. Pass criterion: running `pytest` passes with at least one test for each of FR1.1, FR1.2, FR2.1, FR2.2, FR2.3, FR3.1, FR3.2, FR3.3 and FR4.1.

## Constraints

- The tool uses the standard library only; the tests use `pytest` (NFR1, NFR2).
- The tool is a proof of concept, so packaging for publishing is not part of this work.

## Assumptions

- The tool is run as a Python script (for example `python temp_convert.py --c-to-f 100`) because packaging for publishing is out of scope. Rationale: no installable `temp-convert` command is requested.
- The tool supports Python 3.9 or newer. Rationale: the target environment of the other people who will run it was not stated, so a minimum version is fixed here as a measurable floor.
- The edge-case rules in FR2.1, FR2.2, FR3.1, FR3.2 and FR3.3 (case-insensitive units, end-of-input exit, rejecting non-finite values, `-0.00` shown as `0.00`) come from your request to address the review points on this stage, not from the original intent answers.

## Out of Scope

- Kelvin and any other temperature units (intent-statement).
- Packaging or publishing the tool.

## Open Questions

- Who the reviewers are and whether all of them must agree to accept the proof of concept (intent-statement, stakeholder map).
- The exact operating systems and Python versions the other users run. This does not change the requirements above.
