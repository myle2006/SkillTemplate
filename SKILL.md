---
name: tester-workflow
description: Discover products and test artifacts, plan risk-based testing, design and execute test cases, document defects, and produce evidence-backed QA reports or Tester portfolio content. Use for multi-step software testing workflows; do not use it to assume permission to modify the product when the user only requests testing, diagnosis, or review.
---

# Tester Workflow

Produce QA outcomes traceable from requirements and risks to test cases, executions, defects, and conclusions. Clearly separate observed evidence, inference, and unverified information.

## Select the operating mode

- **Discovery and planning:** read [references/workflow.md](references/workflow.md) and [references/standards.md](references/standards.md).
- **Test case or checklist design:** read workflow, standards, and [references/deliverables.md](references/deliverables.md).
- **Execution, retest, or regression:** read workflow and standards; interact with the target system only when authorized by the request.
- **Defect or test summary:** read standards and deliverables.
- **Tester CV or portfolio:** read deliverables; use only metrics that can be verified from supplied artifacts.

## Core workflow

1. Establish the objective, users, environment, scope, constraints, authorization, and required deliverable. Do not infer permission to mutate data or perform intrusive security, load, or stress testing.
2. Discover the test basis: SRS, user stories, acceptance criteria, UI, API/schema, code, suites, historical reports, and evidence. Use `scripts/discover_qa.py` to inventory metadata before deep inspection when useful.
3. Map features, roles, states, data, and dependencies. Record gaps and contradictions as requirement issues; do not silently turn them into expected results.
4. Prioritize by impact, likelihood, change frequency, exposure, and detectability. Cover appropriate happy paths, negative cases, boundaries, states, authorization, integration, recovery, and non-functional risks.
5. Design test cases with stable IDs, traceability, preconditions, test data, reproducible steps, observable expected checkpoints, priority, and cleanup. Never use the current execution's actual result as its own expected result.
6. When execution is authorized, record the build, environment, device/browser, role, and time. Protect existing data, use isolated fixtures, and clean up only artifacts created by the run. Distinguish `PASS`, `FAIL`, `BLOCKED`, `NOT RUN`, and `ERROR`.
7. Open a defect only when there is a valid expected result, an observed deviation, and a reproducible path. Separate product defects from requirement, automation, configuration, test-data, and environment issues.
8. Report coverage, results, material defects, blockers, residual risks, and limitations. Use `scripts/summarize_results.py` for normalized CSV sources.

## Quality invariants

- Every count or percentage must trace to a file, sheet/range, test report, or log.
- Mark newly designed, unexecuted tests NOT RUN. Convert unspecified constraints into requirement questions; proposed best practices are not approved requirements.
- Keep supplied-record counts separate from total planned scope. Verify contribution evidence before attributing group work to an individual.
- `BUILD SUCCESS`, HTTP 200, or the absence of an exception does not by itself prove that the product passed.
- Blocked tests never count as passes. Partial verification must identify the checkpoints that were and were not verified.
- Severity represents impact; priority represents repair order. Do not treat them as interchangeable.
- Claim security, performance, accessibility, mobile, or cross-browser coverage only for the actual scope, tools, devices, and environments verified.
- For formal compliance, verify the current standard from an authoritative source. The bundled references are operational conventions, not certification evidence.

## Outputs

Select the closest template under `assets/templates/` and preserve its schema unless the user provides another format. Do not create output files when the user requests only an answer, explanation, or review.
