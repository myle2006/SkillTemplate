# Multi-step QA workflow

## 1. Intake and boundaries

Record the objective, target users, build or URL, environment, roles/accounts, permitted data, deadline, and deliverable. Separate read-only investigation from actions that modify the target system.

Do not perform load or stress tests, intrusive vulnerability scans, brute force, real email/notification delivery, role or password changes, deletion of existing data, or bulk account creation without explicit authorization.

## 2. Discovery

Inventory first, then inspect selectively:

1. Requirements: SRS, PRD, user stories, acceptance criteria, wireframes, and API contracts.
2. Product: navigation, roles, states, validation, CRUD, integrations, and file workflows.
3. Implementation evidence: code, schemas, configuration, test suites, CI, and logs.
4. Historical evidence: test cases, defects, screenshots, and prior reports.

Run `python3 scripts/discover_qa.py <root> --format markdown` to inventory metadata. The script does not read credential contents or edit source artifacts.

## 3. Model the system

Create a compact map with `Feature / Role / Input or State / Dependency / Requirement / Risk`. Use a state or sequence diagram only when it materially clarifies branching, handoffs, dependencies, or rollback.

Track requirement issues separately: ambiguity, contradiction, missing validation or error behavior, missing role rules, unmeasurable criteria, and discrepancies between the UI and requirements.

## 4. Risk-based planning

Rate risks as `High/Medium/Low` or 1–5 for:

- Impact: potential user, business, security, or data harm.
- Likelihood: complexity, frequency, and defect history.
- Change and exposure: recent changes, traffic, roles, and integrations.
- Detectability: silent failures, delayed effects, and recovery difficulty.

Prioritize authentication and authorization, money or critical data, core workflows, changed code, integration boundaries, and recovery.

## 5. Test design

Choose techniques based on risk:

- Equivalence Partitioning for inputs expected to behave alike.
- Boundary Value Analysis for meaningful values around minimum and maximum limits.
- Decision Tables for combined rules and conditions.
- State Transition Testing for sessions, status, approvals, progress, retry, and timeout.
- Use-case or scenario testing for end-to-end flows and role/module handoffs.
- Error Guessing or exploratory testing for race conditions, refresh/back, duplicates, network interruption, and historical weak points.

Give each test case one primary objective. Split cases when checkpoints can fail independently or require different setup or cleanup.

## 6. Execution

Before execution, record the build, browser/device, viewport, role/account, seed/fixture, feature flags, and time. Confirm that expected results are independent of the current run.

During execution, record actual results at each checkpoint. Collect URL, timestamp, request/response, logs, video, or screenshots when they help prove the observation. Do not retain unnecessary secrets, tokens, passwords, or personal data.

After execution, remove only fixtures created by the run and record cleanup results. Retest confirmed defects before running related regression coverage.

## 7. Triage and closure

Classify observations as product defects, requirement issues, test-data issues, environment issues, automation issues, or duplicates. When evidence is insufficient, record an observation or candidate issue instead of a confirmed defect.

Exit criteria must match the agreed scope: priority tests executed, no defects above the accepted threshold, relevant regression completed, residual risks accepted, and evidence traceable.
