# Cross-Unit Traceability

Output of `aidlc engine sensor-traceability --stage build-and-test`. Source documents: `code-generation-plan.md`, `unit-test-instructions.md` and `code-summary.md` under `aidlc/spaces/default/intents/261114-temperature-converter/construction/code-generation/`. This scope has no separate Units, so everything is built in the one Code Generation pass.

**Verdict: pass.** No requirement is uncovered.

| ID | Covered | Built in | Test |
|----|---------|----------|------|
| FR1.1 | Yes | code-generation: `temp_convert.py` | `test_c_to_f_one_shot`, `test_c_to_f_exponent_form` |
| FR1.2 | Yes | code-generation: `temp_convert.py` | `test_f_to_c_one_shot` |
| FR2.1 | Yes | code-generation: `temp_convert.py` | `test_interactive_converts` |
| FR2.2 | Yes | code-generation: `temp_convert.py` | `test_interactive_exit_forms` |
| FR2.3 | Yes | code-generation: `temp_convert.py` | `test_interactive_bad_input_reprompts` |
| FR3.1 | Yes | code-generation: `temp_convert.py` | `test_bad_value_one_shot`, `test_logic_parse_finite` |
| FR3.2 | Yes | code-generation: `temp_convert.py` | `test_bad_invocation` |
| FR3.3 | Yes | code-generation: `temp_convert.py` | `test_negative_zero_normalised` |
| FR4.1 | Yes | code-generation: `temp_convert.py` | `test_help_text` |
| NFR1 | Yes | code-generation: `temp_convert.py` | import check (see the Target Verification Matrix) |
| NFR2 | Yes | code-generation: `test_temp_convert.py` | the `pytest` run |

## Uncovered elements

None.
