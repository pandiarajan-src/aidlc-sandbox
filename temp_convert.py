"""Temperature converter between Celsius and Fahrenheit.

One-shot use:
    python temp_convert.py --c-to-f 100     # prints 212.00
    python temp_convert.py --f-to-c 212     # prints 100.00

Interactive use (no arguments): type a value and a unit such as ``100 C`` or
``212 F`` and the converted value is printed in the other unit, rounded to two
decimals. Enter ``q``, an empty line, or end-of-input to quit.

Bad input writes a short message to standard error and (one-shot) exits with a
non-zero code. Standard library only.
"""

import argparse
import math
import re
import sys

_EPILOG = """\
Run with no arguments to start interactive mode: enter a value and a unit
(for example "100 C" or "212F"); enter q, Q, an empty line or end-of-input
to quit.

examples:
  python temp_convert.py --c-to-f 100    prints 212.00
  python temp_convert.py --f-to-c 212    prints 100.00
"""

_INTERACTIVE_RE = re.compile(r"^(?P<value>.+?)\s*(?P<unit>[cCfF])$")


def c_to_f(celsius):
    """Convert degrees Celsius to degrees Fahrenheit."""
    return celsius * 9.0 / 5.0 + 32.0


def f_to_c(fahrenheit):
    """Convert degrees Fahrenheit to degrees Celsius."""
    return (fahrenheit - 32.0) * 5.0 / 9.0


def format_result(value):
    """Format with 2 decimals; a result that rounds to zero prints ``0.00``."""
    text = f"{value:.2f}"
    if text == "-0.00":
        return "0.00"
    return text


def parse_finite(text):
    """Parse text into a finite float, or raise ValueError.

    Underscores are rejected: float() accepts digit-group underscores (1_0).
    Non-ASCII text is rejected: float() accepts non-ASCII Unicode digits.
    """
    if "_" in str(text) or not str(text).isascii():
        raise ValueError(f"not a number: {str(text).strip()!r}")
    try:
        value = float(text)
    except (TypeError, ValueError):
        raise ValueError(f"not a number: {str(text).strip()!r}") from None
    if not math.isfinite(value):
        raise ValueError(f"not a finite number: {str(text).strip()!r}")
    return value


def _convert(value, unit):
    """Convert value from unit ('C' or 'F'); reject a non-finite result."""
    result = c_to_f(value) if unit == "C" else f_to_c(value)
    if not math.isfinite(result):
        raise ValueError("result is too large to represent")
    return result


class _UsageError(Exception):
    pass


class _Parser(argparse.ArgumentParser):
    """ArgumentParser that writes to injected streams and never exits."""

    out = None
    err = None

    def error(self, message):
        raise _UsageError(message)

    def exit(self, status=0, message=None):
        if message:
            self.err.write(message)
        raise SystemExit(status)

    def _print_message(self, message, file=None):
        if message:
            (self.err if file is sys.stderr else self.out).write(message)


def _build_parser(stdout, stderr):
    parser = _Parser(
        prog="temp_convert.py",
        description="Convert temperatures between Celsius and Fahrenheit.",
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )
    parser.out = stdout
    parser.err = stderr
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--c-to-f", metavar="VALUE", help="convert VALUE from Celsius to Fahrenheit")
    group.add_argument("--f-to-c", metavar="VALUE", help="convert VALUE from Fahrenheit to Celsius")
    return parser


def _interactive(stdin, stdout, stderr):
    while True:
        stdout.write("> ")
        stdout.flush()
        line = stdin.readline()
        if line == "":  # end-of-input
            stdout.write("\n")
            return 0
        text = line.strip()
        if text == "" or text.lower() == "q":
            return 0
        match = _INTERACTIVE_RE.match(text)
        if not match:
            stderr.write(f"error: expected a number followed by C or F, got {text!r}\n")
            continue
        try:
            value = parse_finite(match.group("value"))
        except ValueError:
            stderr.write(f"error: expected a finite number followed by C or F, got {text!r}\n")
            continue
        try:
            result = _convert(value, match.group("unit").upper())
        except ValueError as exc:
            stderr.write(f"error: {exc}\n")
            continue
        unit_out = "F" if match.group("unit").upper() == "C" else "C"
        stdout.write(f"{format_result(result)} {unit_out}\n")


def main(argv=None, stdin=None, stdout=None, stderr=None):
    """Run the CLI; return the process exit code."""
    argv = sys.argv[1:] if argv is None else list(argv)
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr

    parser = _build_parser(stdout, stderr)
    try:
        args = parser.parse_args(argv)
    except _UsageError as exc:
        stderr.write(f"temp_convert.py: error: {exc}\n")
        return 2
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 0

    if args.c_to_f is None and args.f_to_c is None:
        return _interactive(stdin, stdout, stderr)

    text, unit = (args.c_to_f, "C") if args.c_to_f is not None else (args.f_to_c, "F")
    try:
        result = _convert(parse_finite(text), unit)
    except ValueError as exc:
        stderr.write(f"error: {exc}\n")
        return 1
    stdout.write(format_result(result) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
