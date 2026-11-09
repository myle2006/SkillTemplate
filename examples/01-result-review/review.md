# Before/after: reporting test results

Synthetic demonstration. The suggested draft and review decisions below illustrate the intended reviewer workflow; they are not a recorded human conversation.

## Input

`results.csv` contains five unique tests from one simulated run: two PASS, one FAIL, one BLOCKED, and one NOT RUN. No requirement coverage matrix or individual contribution record is supplied.

## Before: illustrative AI suggestion

> Executed all five tests with an 80% pass rate and full coverage. Personally automated the complete suite and confirmed readiness for release.

## Reviewer decisions

| Suggestion | Decision | Reason |
|---|---|---|
| Summarize the five test records | Keep | Five unique records are present. |
| All five executed | Reject | One was not run; another was blocked. |
| 80% pass rate | Reject | Only two tests passed; blocked and unrun tests cannot become passes. |
| Full coverage | Reject | No requirement denominator or traceability matrix exists. |
| Personal automation ownership | Reject | The CSV contains no authorship or implementation evidence. |
| Ready for release | Reject | Exit criteria and accepted residual risks were not supplied. |

## After: reviewed output

> Five test records were supplied: two passed, one failed, one was blocked, and one was not run. Pass rate among conclusive product results is 2 / (2 + 1) = 66.7%. Four records were attempted under the convention that includes blocked attempts. Requirement coverage, personal contribution, and release readiness remain unverified.

## Reproduce the numeric check

```sh
python3 scripts/summarize_results.py examples/01-result-review/results.csv
```

## Template lesson

State the denominator, distinguish supplied records from planned scope, and request separate evidence for coverage and ownership. These checks are now explicit in the skill and reporting guidance.
