# Before/after: invented validation rules

Synthetic demonstration using `input.md`. The AI draft and reviewer decisions are illustrative, not a historical transcript.

## Before: illustrative AI suggestion

> Reject passwords shorter than eight characters, require uppercase and special characters, and lock accounts after three failed attempts. Missing enforcement is a High-severity defect. The generated tests passed.

## Reviewer decisions

| Suggestion | Decision | Reason |
|---|---|---|
| Test active-user login | Keep | Directly supported by REQ-LOGIN-01. |
| Test incorrect credentials | Keep | Directly supported by REQ-LOGIN-02. |
| Eight-character minimum and composition rules | Reject as requirements | No approved policy was supplied. They may be proposed for clarification. |
| Three-attempt lockout | Reject as requirement | The threshold and recovery behavior are unspecified. |
| Confirmed High-severity defect | Reject | There is neither an approved expected rule nor observed product behavior. |
| Tests passed | Reject | Design alone supplies no execution evidence. |

## After: reviewed output

| ID | Requirement | Scenario | Expected result | Status |
|---|---|---|---|---|
| TC-LOGIN-01 | REQ-LOGIN-01 | Sign in with an active user's valid credentials | Authentication succeeds | NOT RUN |
| TC-LOGIN-02 | REQ-LOGIN-02 | Submit incorrect credentials | No authenticated session is created | NOT RUN |

Open questions: What password policy applies? Is lockout or rate limiting required, and with what recovery behavior? Is exact error text prescribed? Record answers as approved requirements before adding their assertions.

## Template lesson

Distinguish requirements, proposed best practices, and observations. Unknown values remain unresolved; generated test cases start as NOT RUN.
