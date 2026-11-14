# Code Generation Plan

## Summary

- Builds: a small Python command-line temperature converter (Celsius and Fahrenheit) with a simple interactive mode
- Touches: `temp_convert.py` and `test_temp_convert.py` at the project root (two new files; nothing existing is changed)
- Tests: 9 requirement-driven unit tests with `pytest` (one per FR sub-requirement group, some parametrized)

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "org",
  "ordering": "implement each applicable testable layer, then write and run that layer's tests.",
  "scope": "poc",
  "test_strategy": "minimal",
  "project_type": "greenfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop`, `classic` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    }
  ],
  "obligations": {
    "strategy": "minimal",
    "strategy_volume": [
      "One verifiable test per requirement at the narrowest effective level.",
      "At least one happy-path unit test per component.",
      "Unit tests are the default; a bugfix/security scope floor may require an integration or E2E regression when that is the narrowest level that reproduces the defect."
    ],
    "scope_floor": [
      "Keep the existing test suite green.",
      "This scope adds no extra new-test floor beyond the selected test strategy."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:8ea1ef920e68ca73437a39f413355d71d0d909a57d5d857da31deb5d9355e261",
  "contract_sha256": "sha256:615d0f211ddcd07aebccb0dd6a68c9e4b811c5fab93b04a37004687ace5379de"
}
```

## Steps

- [ ] Step 1: Project structure. Create `temp_convert.py` (the tool) and `test_temp_convert.py` (the tests) at the project root. No other files are added. Implements NFR1 (standard library only).
- [ ] Step 2: Test runner readiness. `pytest` is the runner (NFR2); no configuration file is needed. Unit-scoped command: `python -m pytest test_temp_convert.py -q`. Recorded in `unit-test-instructions.md`.
- [ ] Step 3: Business logic, implement. In `temp_convert.py`: `c_to_f`, `f_to_c`, `format_result` (2 decimals, `-0.00` shown as `0.00`), and `parse_finite` (rejects text, `nan`, `inf`, and overflow). Implements FR1.1, FR1.2, FR3.1, FR3.3.
- [ ] Step 4: Business logic, write and run its tests. Tests for FR1.1, FR1.2, FR3.1 (parsing and overflow) and FR3.3 in `test_temp_convert.py`.
- [ ] Step 5: Command-line layer, implement. In `temp_convert.py`: `main(argv, stdin, stdout, stderr)` using `argparse` with a mutually exclusive `--c-to-f` / `--f-to-c` pair, `--help` with examples and the interactive-mode note, and an interactive loop (value and unit like `100 C`, case-insensitive unit, optional space, exit on `q`, `Q`, an empty line or end-of-input). Bad input and bad invocations write a short message to standard error and exit non-zero. Implements FR1.1, FR1.2, FR2.1, FR2.2, FR2.3, FR3.1, FR3.2, FR4.1.
- [ ] Step 6: Command-line layer, write and run its tests. Tests for FR2.1, FR2.2, FR2.3, FR3.1, FR3.2 and FR4.1 through `main(...)` with in-memory streams.
- [ ] Step 7: Documentation. Module docstring and the `--help` text in `temp_convert.py`; run notes go in `code-summary.md`. The project's existing files (`.gitignore`, `.mcp.json`) are left as they are.
- [ ] Step 8: Requested changes (review points R-01 to R-03). In `temp_convert.py`, `parse_finite` rejects values containing an underscore (so `--c-to-f 1_0` is bad input, FR3.1). In `test_temp_convert.py`, add `1e999` and `1_0` to the bad-value tests, add an exponent-form success test (`--c-to-f=-1e2` prints `-148.00`, FR1.1), and make the interactive exit test assert that nothing after `q`, `Q` or an empty line is converted (FR2.2). Run `.venv/bin/python -m pytest test_temp_convert.py -q`.

- [x] Step 9: Requested change (review point R-04). In `temp_convert.py`, `parse_finite` rejects values that contain non-ASCII characters (so non-ASCII digits such as Arabic-Indic `١٠٠` are bad input, FR3.1). In `test_temp_convert.py`, add one non-ASCII-digit value to the bad-value tests (unit and one-shot). Run `.venv/bin/python -m pytest test_temp_convert.py -q`.

## Requirement Traceability

| Requirement | Plan steps | Test |
|-------------|-----------|------|
| FR1.1 | 3, 5 | `test_c_to_f_one_shot` |
| FR1.2 | 3, 5 | `test_f_to_c_one_shot` |
| FR2.1 | 5 | `test_interactive_converts` |
| FR2.2 | 5 | `test_interactive_exit_forms` |
| FR2.3 | 5 | `test_interactive_bad_input_reprompts` |
| FR3.1 | 3, 5 | `test_bad_value_one_shot` |
| FR3.2 | 5 | `test_bad_invocation` |
| FR3.3 | 3 | `test_negative_zero_normalised` |
| FR4.1 | 5 | `test_help_text` |
| NFR1 | 1 | checked by the imports in `temp_convert.py` (standard library only) |
| NFR2 | 2, 4, 6 | the `pytest` run itself |
