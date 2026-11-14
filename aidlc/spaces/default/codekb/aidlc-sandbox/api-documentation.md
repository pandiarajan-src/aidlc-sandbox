# API Documentation

## CLI (`python temp_convert.py`)
| Invocation | Behaviour | Exit |
|---|---|---|
| `--c-to-f VALUE` | prints Fahrenheit, 2 decimals | 0 |
| `--f-to-c VALUE` | prints Celsius, 2 decimals | 0 |
| (no arguments) | interactive prompt `> `; input `<number> <C\|F>`, case-insensitive | 0 on `q`, empty line, or EOF |
| invalid value | message on stderr | 1 |
| invalid flags | message on stderr | 2 |
The two flags are mutually exclusive. `--help` prints usage on stdout with exit 0.

## Python functions (`temp_convert.py`)
| Function | Contract |
|---|---|
| `c_to_f(celsius)` | `celsius * 9.0 / 5.0 + 32.0` |
| `f_to_c(fahrenheit)` | `(fahrenheit - 32.0) * 5.0 / 9.0` |
| `format_result(value)` | `f"{value:.2f}"`, with `-0.00` mapped to `0.00` |
| `parse_finite(text)` | finite float, or `ValueError` (non-ASCII, underscore, nan/inf, non-numeric) |
| `main(argv, stdin, stdout, stderr)` | returns the exit code |
Private: `_convert`, `_build_parser`, `_interactive`, `_Parser`, `_UsageError`.

No network, database, or external APIs.
