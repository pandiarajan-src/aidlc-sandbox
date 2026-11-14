# Business Overview

## Purpose
A small Python command-line tool that converts temperatures between Celsius and Fahrenheit, printing results rounded to two decimals.

## Key Functionality
- One-shot: `--c-to-f VALUE` and `--f-to-c VALUE` print one result and exit.
- Interactive: with no arguments, a prompt loop accepts input such as `100 C` or `212F` until `q`, an empty line, or end-of-input.
- Bad input prints a short message to stderr; one-shot mode exits non-zero.

## Users
Anyone running the script from a shell. There is no service, UI, or persistence.

## Current Concern
Active intent `celsius-sign-bug` reports that -40 C returns the wrong sign. See `code-quality-assessment.md` for the finding.
