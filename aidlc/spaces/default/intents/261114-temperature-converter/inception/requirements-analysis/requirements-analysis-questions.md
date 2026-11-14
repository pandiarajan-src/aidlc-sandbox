# Requirements Analysis Questions

## Q1. [Product] How should someone run a single conversion from the command line?

The intent says other people will run the tool and it needs clear usage help. This fixes the command shape the tests and the help text will describe.

A. `temp-convert 100 C` (a number followed by the unit it is in; the tool prints the converted value in the other unit)
B. `temp-convert 100 --from C --to F` (explicit source and target flags)
C. `temp-convert --c-to-f 100` / `temp-convert --f-to-c 212` (one flag per direction)
D. Not yet defined
X. Other (please specify)

[Answer]: C. `temp-convert --c-to-f 100` / `temp-convert --f-to-c 212` (one flag per direction)

## Q2. [Product] How should the simple interactive mode behave?

The intent includes a simple interactive mode in this first version. This sets what it does and how someone leaves it.

A. Run with no arguments: it repeatedly asks for a value and unit (like `100 C`), prints the result, and exits on `q` or an empty line
B. Run with an `-i` flag: same prompt loop as A, but only when the flag is given
C. Not yet defined
X. Other (please specify)

[Answer]: A. Run with no arguments: it repeatedly asks for a value and unit (like `100 C`), prints the result, and exits on `q` or an empty line

## Q3. [Developer] How should results be rounded, and how should bad input be handled?

The intent says conversions must be correct; this makes "correct" checkable (for example 100 C = 212.0 F).

A. Print the result rounded to 2 decimal places; for bad input (not a number, unknown unit) print a short message to standard error and exit with a non-zero code
B. Print the full-precision result; for bad input print a short message to standard error and exit with a non-zero code
C. Not yet defined
X. Other (please specify)

[Answer]: A. Print the result rounded to 2 decimal places; for bad input (not a number, unknown unit) print a short message to standard error and exit with a non-zero code

## Q4. [Developer] Which tools may the tool and its unit tests depend on?

This decides whether anyone needs to install anything beyond Python to run the tool and its tests.

A. Python standard library only, with tests written using `unittest` (nothing to install)
B. Python standard library for the tool, with tests written using `pytest`
C. Not yet defined
X. Other (please specify)

[Answer]: B. Python standard library for the tool, with tests written using `pytest`

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
