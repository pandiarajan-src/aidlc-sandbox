# Code Structure

## Layout
```
./
  temp_convert.py        source: CLI and conversion logic (174 lines)
  test_temp_convert.py   tests: pytest (138 lines)
  .gitignore             ignore rules
```
There are no packages or subdirectories of project code.

## File Classification
| File | Class |
|---|---|
| `temp_convert.py` | service/utility + CLI entry point |
| `test_temp_convert.py` | test |

## Code Patterns
- Pure functions for conversion and formatting; side effects confined to `main` and `_interactive`.
- Dependency injection of stdin/stdout/stderr.
- Leading-underscore names mark private helpers.
- `if __name__ == "__main__": sys.exit(main())` entry point.
