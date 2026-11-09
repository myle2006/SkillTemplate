# Version notes

## 1.1.0 — 2026-11-09

Prepared the package for a public portfolio repository with an English README, two synthetic before/after reviews, and executable regression checks.

### Observed implementation error and correction

The initial summarizer counted every input row as a planned test and accepted duplicate Test Case IDs. Two rows with the same ID and PASS status could therefore produce “Planned records: 2” and a 100% pass rate, even though the file did not establish two distinct tests or a complete plan. Unknown status values were also retained without stopping the report.

Correction: require unique, nonempty IDs, reject malformed CSV rows and unknown or missing statuses, normalize supported status aliases, and report “Supplied test records.” Explicitly state pass-rate exclusions and that coverage and planned scope cannot be inferred from CSV alone. Optional defect inputs also require unique IDs.

Verification: regression tests cover duplicates, missing/unknown statuses, malformed rows, aliases, blocked/unrun exclusions, and empty datasets. Run `python3 -m unittest discover -s tests -v`.

### Hallucination-focused template changes

The review examples demonstrate two failure modes: inventing successful execution/coverage and inventing password rules. These are synthetic review exercises, not claimed incidents from an actual model run. The skill now explicitly requires NOT RUN for unexecuted designs, requirement questions for unspecified constraints, and separate proof for ownership and coverage.

### Validation precision

Earlier structural checks were a limited fallback, not equivalent to the bundled official validator. That validator previously failed to start because PyYAML was unavailable. This repository does not claim that fallback checks establish full official validation.

## 1.0.0 — 2026-11-09

Initial English skill with workflow routing, QA conventions, discovery and summarization helpers, and five output templates. Demonstration rows were included in CSV templates. Helper smoke checks passed; the official skill validator was unavailable because its Python environment lacked PyYAML.
