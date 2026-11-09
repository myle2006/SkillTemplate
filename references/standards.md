# QA operating conventions

This reference uses ISTQB terminology and work-product structures inspired by ISO/IEC/IEEE 29119. It is neither a copy of a standard nor evidence of compliance. For formal compliance, verify the current official publication.

## Test statuses

| Status | Definition |
|---|---|
| PASS | Every planned checkpoint executed and actual results matched expected results. |
| FAIL | At least one checkpoint showed an observable product deviation. |
| BLOCKED | Execution could not finish because of a prerequisite, permission, data, device, or dependency. |
| NOT RUN | Execution has not started. |
| ERROR | Infrastructure, tooling, automation, configuration, or cleanup failed; no product conclusion is available. |

## Severity

| Level | Operating convention |
|---|---|
| Critical | Severe data loss/corruption, critical security exposure, or system unusable without a workaround. |
| High | Core workflow or authorization failure, broad user impact, or poor workaround. |
| Medium | Secondary function fails, or a core flow has an acceptable workaround. |
| Low | Limited UI, content, or usability impact. |

Priority depends on business timing, release scope, affected users, and repair cost; it may differ from severity.

## Defect Definition of Ready

A defect is ready for triage when it contains: ID, specific title, build/environment, role, preconditions, data, minimal reproduction steps, a test-basis-backed expected result, observed actual result, reproducibility, reasoned severity and priority, and evidence with secrets and personal data removed.

Use a title such as `[Area] Incorrect behavior when condition`. Avoid titles such as `Does not work`.

## Traceability and coverage

Maintain at least `Requirement or Risk → Test Case → Run Result → Defect`. Coverage is measured against a defined set; pass rate is not a substitute for coverage.

Use `PASS / (PASS + FAIL)` for pass rate only when exclusions such as BLOCKED and NOT RUN are stated. Use `(PASS + FAIL + BLOCKED + ERROR) / Total planned` for execution rate.

## Security, accessibility, and performance

- Security: use OWASP WSTG or ASVS as a design source when appropriate; do not execute destructive payloads or intrusive scans without authorization.
- Accessibility: when requested, cover keyboard operation, focus, name/role/value, contrast, zoom/reflow, and relevant screen-reader behavior; state the target WCAG version.
- Performance: require an approved workload, concurrency, duration, dataset, environment, and threshold. Do not infer performance from visual responsiveness alone.

## Evidence

Evidence should prove the relevant checkpoint, include time/build/URL when material, and show the deviation clearly. A screenshot does not replace network, console, database, or video evidence when the behavior exists only in those channels.
