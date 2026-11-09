# Deliverable conventions

## Template routing

| Need | Template |
|---|---|
| Strategy and scope | `assets/templates/test-plan.md` |
| Importable test cases | `assets/templates/test-cases.csv` |
| Importable defects | `assets/templates/defect-report.csv` |
| Execution report | `assets/templates/test-summary.md` |
| Tester portfolio or CV | `assets/templates/tester-project-cv.md` |

If the user supplies a template, preserve its schema and terminology unless doing so would change the meaning of the data.

## Test cases

- Use stable IDs that do not depend on row numbers.
- Populate `Requirement or Risk` when a test basis exists.
- Start steps with verbs and make each action reproducible.
- Describe observable expected results; avoid phrases such as `works correctly`.
- Store sensitive data in placeholders or a secret store, not in a workbook or repository.

## Defects

Each defect should prove one primary deviation. Do not combine symptoms under an assumed root cause. Record reproducibility as `3/3`, `Intermittent 2/5`, or `Not retested`.

## Test summaries

The lead statement should identify the tested build and scope, how much was executed, material defects or blockers, and whether a recommendation can be made. Do not add a release recommendation when the user asks only for metrics.

## Tester CV and portfolio

Use three to five bullets per project: product and scope, individual contribution, techniques and tools, verified scale, and evidence-backed outcome. Use `Participated in` for group work when ownership cannot be verified. Do not add overlapping suites or historical executions into an inflated total.
