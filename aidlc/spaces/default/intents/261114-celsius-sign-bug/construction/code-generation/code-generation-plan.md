# Code Generation Plan

## Summary

- Builds: regression tests that pin -40 and other negative values in both directions, and a small change so a one-shot flag accepts a negative number in any written form without `=`
- Touches: `temp_convert.py` (one small helper called from `main`) and `test_temp_convert.py` (new tests added; no existing test changed)
- Tests: about 8 new `pytest` test functions (several parametrized) on top of the existing 40, which stay green

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "org",
  "ordering": "implement each applicable testable layer, then write and run that layer's tests.",
  "scope": "bugfix",
  "test_strategy": "minimal",
  "project_type": "brownfield",
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
      "Include a targeted regression for the bug or vulnerability.",
      "Keep the existing test suite green."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Verify the existing test runner/configuration and record the exact unit-scoped command.",
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
      "Verify the existing test runner/configuration and record the exact unit-scoped command.",
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
  "input_sha256": "sha256:bf575ef6e849a46084d60d2a1978cd105f337233b9e6f61c9518f1621d13d958",
  "contract_sha256": "sha256:fcb111e060b3a6ede81676e117b560f8eab5d852833d5fab1b8adaef534afbb8"
}
```

## Steps

- [x] Step 1: Project structure. No new files. The change stays in `temp_convert.py` and `test_temp_convert.py` (the two files `requirements.md` limits the work to). Implements NFR1 (standard library only).
- [x] Step 2: Test runner readiness. `pytest` is already installed in the project's `uv` virtual environment (`.venv`). Unit-scoped command: `.venv/bin/python -m pytest test_temp_convert.py -q`. Recorded in `unit-test-instructions.md`.
- [x] Step 3: Observe before changing anything (answers review points R-01 and R-02). With separate commands and no edits, run `--c-to-f -1e2`, `--c-to-f -.5`, `--c-to-f -inf` and `--c-to-f -40` on the `.venv` interpreter (Python 3.14.8) and on Python 3.9 (`/usr/bin/python3`), and record the exit code and output of each in `code-summary.md`. This shows on which interpreters FR2.1 changes behaviour.
- [x] Step 4: Business logic, implement. In `temp_convert.py`, add a small helper, `_join_negative_values(argv)`, and call it in `main` before `parse_args`. When `--c-to-f` or `--f-to-c` is followed by a token that starts with a single `-` (not `--`, and not `-h`), the helper joins the two into `--c-to-f=<token>`. The joined value then goes through the existing `parse_finite`, so `-inf`, `-nan`, `-`, `-1_0` and non-ASCII text are rejected as bad input with exit code 1 and a short message on standard error. Nothing about conversion, rounding or interactive mode changes. Implements FR2.1, FR2.2, FR2.3 (and the sign handling behind FR1).
- [x] Step 5: Business logic, write and run its tests. In `test_temp_convert.py`, add tests through `main(...)` with in-memory streams, plus direct calls:
  - FR1.1: `-40` gives `-40.00` in both directions with the value as a separate argument, with `=`, in interactive mode (`-40 C`, `-40C`, `-40 F`, `-40f`), and through `c_to_f` and `f_to_c`.
  - FR1.2: `--c-to-f -10` prints `14.00` and `--f-to-c -10` prints `-23.33`.
  - FR2.1: `--c-to-f -1e2` prints `-148.00` and `--c-to-f -.5` prints `31.10`.
  - FR2.2: `--c-to-f -inf` and `--f-to-c -nan` print nothing to standard output, write a message to standard error, and exit non-zero.
  - FR2.3: the existing 40 tests run unchanged and stay green.
  Each test asserts the exact printed text, so a flipped sign in the result fails it.
- [x] Step 6: Run the whole suite on `.venv` (Python 3.14.8) and on Python 3.9 in a temporary `uv` virtual environment (removed afterwards), and record both results in `code-summary.md`. Covers NFR1.
- [x] Step 7: Documentation and traceability. Run notes and the observations from Step 3 go in `code-summary.md`; the `--help` text and docstring only change if Step 4 makes them wrong. Closing note for the original report (review point R-06): the converter returns `-40.00` for -40 C and -40 F because the two scales meet at -40; the note goes in `code-summary.md`.

## Requirement Traceability

| Requirement | Plan steps | Test |
|-------------|-----------|------|
| FR1.1 | 5 | `test_minus_40_both_directions`, `test_minus_40_equals_form`, `test_minus_40_interactive`, `test_minus_40_functions` |
| FR1.2 | 5 | `test_other_negative_values` |
| FR2.1 | 3, 4, 5 | `test_negative_exponent_and_decimal_forms` |
| FR2.2 | 4, 5 | `test_negative_non_finite_rejected` |
| FR2.3 | 4, 5 | the existing 40 tests, unchanged |
| NFR1 | 1, 4, 6 | checked by the imports in `temp_convert.py` and the Python 3.9 run |
| NFR2 | 2, 5, 6 | the `pytest` runs themselves, through `uv` |
