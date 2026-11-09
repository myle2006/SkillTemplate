# Tester Workflow

A reusable AI skill for software testers: discover the test basis, plan coverage by risk, design tests, review execution evidence, and produce traceable QA deliverables.

This portfolio project demonstrates QA judgment alongside AI assistance. The reviewer checks expected results, accepts useful suggestions, rejects unsupported claims, and records why the template changes after errors.

## What it is for

- Manual and automation test planning and test case design.
- Reviewing requirements, test results, and defect reports.
- Summarizing execution evidence and residual risks.
- Drafting Tester project descriptions for a CV from verified work.

The helper scripts inventory files and summarize supplied results. They do not execute browser tests or autonomously operate a live application; the AI needs appropriate tools and authorized access for execution.

## Inputs and outputs

| Input | Output |
|---|---|
| SRS, user stories, acceptance criteria, constraints | Test plan, requirement questions, risk priorities |
| Feature descriptions, roles, states, test data | Test cases with requirement links and expected results |
| One run of results, environment details, evidence | Test summary with explicit denominators and limitations |
| Reproduction steps and observed deviations | Defect report with severity, priority, and evidence |
| Verified project artifacts and personal contribution | CV/portfolio project bullets |

Supported helper inputs: local directories; `.xlsx`/`.xlsm` workbook metadata; selected XML test reports; UTF-8 CSV results. Python 3.10 or newer is required. Both helpers use the standard library only.

## How to use

Give an AI agent `SKILL.md` as the entry point and supply the relevant artifacts. The entry point routes it to the needed references. Automatic discovery depends on installation in the host's skill directory; merely uploading this repository does not activate it.

Example request:

> Use tester-workflow to review the supplied SRS and design tests for login. Produce a test plan and test cases. List ambiguous requirements before proposing expected results. Scope: local document analysis only.

Run the helper scripts from the repository root:

```sh
python3 scripts/discover_qa.py examples --format markdown
python3 scripts/summarize_results.py examples/01-result-review/results.csv
python3 -m unittest discover -s tests -v
```

Use `--output <new-path>` to save a helper result. That option overwrites an existing output file, so select a new output path. Source files are read without modification.

Results CSV requires a unique `Test Case ID` and `Status` (or `Result`/`Test Status`). Accepted statuses: `PASS`, `FAIL`, `BLOCKED`, `ERROR`, `NOT RUN`; aliases: `PASSED`, `FAILED`, `NOT_RUN`. Use one run per file and unique dataset-specific IDs for data-driven invocations. Unknown statuses and duplicate IDs cause an error. The optional `--defects` CSV requires unique `Defect ID` values; severity is reported as supplied, with missing values marked `UNSPECIFIED`.

## Guardrails

- Every metric needs a source and a defined denominator. A test case designed is not a test case executed.
- Blocked tests do not count as passes. Test pass rate does not establish requirement coverage.
- Expected results come from an approved test basis. Unspecified limits become questions, not invented rules.
- Product defects, requirement gaps, automation errors, and environment issues are distinguished.
- Group work does not establish individual ownership; CV claims require personal contribution evidence.
- Live system mutations and intrusive tests require authorization within the task's scope.
- Evidence should exclude credentials, tokens, and unnecessary personal data.
- Bundled conventions are not a claim of ISTQB certification or formal ISO compliance.

## Before/after review examples

1. [Result reporting: reject an inflated pass claim](examples/01-result-review/review.md).
2. [Requirement review: reject invented validation rules](examples/02-requirement-review/review.md).

Both examples are synthetic demonstrations, with explicit input, suggested draft, keep/reject decisions, rationale, and corrected output. They are not transcripts of a human review or claims about a production project. A separate real implementation error reproduced during this revision is documented in [CHANGELOG.md](CHANGELOG.md).

## Repository layout

```text
SKILL.md                 AI workflow entry point
agents/openai.yaml       Host UI metadata
references/              Workflow and QA conventions
assets/templates/        Reusable output templates
scripts/                 Discovery and result summarization
examples/                Synthetic inputs and review decisions
tests/                   Regression checks for result integrity
CHANGELOG.md             Errors, corrections, and verification
```

## Validation and limitations

Run the unittest command above to reproduce the result-integrity checks. Discovery classifies filenames heuristically; it does not prove document content, authorship, or test execution. It excludes hidden directories and common build directories, including `target`, so it may omit generated reports. Workbook inspection lists sheet names, not test-case counts. No live website, security scan, or performance test is part of this repository's validation.

Template CSV rows are examples. Replace them before reporting real results; the summarizer cannot determine whether a plausible record is synthetic.
