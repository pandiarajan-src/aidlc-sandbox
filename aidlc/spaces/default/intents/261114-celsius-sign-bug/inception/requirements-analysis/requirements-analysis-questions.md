# Requirements Analysis Questions

Before these questions, I ran the converter on the current code. `--c-to-f -40`, `--c-to-f -40.0`, `--c-to-f=-40` and `--f-to-c -40` all print `-40.00`, and `-40 C`, `-40C` and `-40 f` in interactive mode print `-40.00 F`, `-40.00 F` and `-40.00 C`. I could not reproduce a wrong sign.

## Q1. [Product] What exactly did you see when you converted -40 C?

The code gives -40.00 for -40 C (which is also -40 F, the point where both scales agree), so I need to know what you saw to find the defect. This decides what the fix must change.

A. A positive number (for example `40.00`) instead of `-40.00`
B. The right size but the wrong sign for a different value (not -40), such as `-10 C` or `-17.78 C`
C. An error message or usage text instead of a result
D. Not sure; someone else reported it and I do not have the output
X. Other (please specify)

[Answer]: X. I get -40.00 F, I think it is correct

## Q2. [Developer] Where did you run the conversion?

The tool has more than one way in, and each reads a negative number through different code. This tells me which path to check first.

A. One-shot command line, such as `python temp_convert.py --c-to-f -40`
B. Interactive mode (run with no arguments), such as typing `-40 C`
C. Calling `c_to_f` or `f_to_c` from other Python code
D. A different copy or version of the tool than the one in this folder
X. Other (please specify)

[Answer]: B. Interactive mode

## Q3. [Product] If the sign bug cannot be reproduced in this code, what should this fix deliver?

A bug fix needs a regression test either way. This sets what counts as done when the code already looks correct.

A. Add regression tests for -40 C and -40 F through every way in (one-shot, `=` form, interactive, the two functions), change no tool code, and tell me what I should check on my side
B. The same as A, and also make negative-number input more forgiving if any path turns out to be fragile
C. Stop here and close the report as not reproducible
X. Other (please specify)

[Answer]: B. The same as A, and also make negative-number input more forgiving if any path turns out to be fragile
