# Scenario Map

Use this file to choose the right example bundle quickly.

## Contract baseline

- Purpose: understand the repository's core three-artifact contract shape
- Artifacts:
  - `interception-policy.example.json`
  - `handover-packet.example.json`
  - `review-decision.example.json`
- Best for: schema-first implementation, validator testing, API contract work

## Bug fix supervision

- Purpose: narrow, high-risk production patch with constrained scope
- Artifacts:
  - `bug-fix-handover-packet.example.json`
  - `bug-fix-report.example.md`
  - `bug-fix-review-decision.example.json`
- Reviewer profile: engineering approver
- Best for: production defect response, low-confidence automated fixes

## Feature implementation supervision

- Purpose: new capability with product, privacy, and rollout considerations
- Artifacts:
  - `feature-implementation-handover-packet.example.json`
  - `feature-implementation-report.example.md`
  - `feature-implementation-review-decision.example.json`
- Reviewer profile: product or security approver
- Best for: new feature work, export or data exposure changes

## Report-only high-risk engineering scenarios

- `risky-refactor-report.example.md`
- `dependency-upgrade-report.example.md`
- `database-migration-report.example.md`
- `payment-logic-change-report.example.md`
- `auth-permissions-change-report.example.md`

Use these when you want reviewer-facing markdown examples for specific software-engineering risk classes without a full JSON packet bundle.

## Anti-pattern and validator coverage

- `negative-handover-examples.md`: bad human handovers and why they fail
- `invalid/`: intentionally invalid machine-readable fixtures for validator checks

## Picking A Starting Point

- Start with the contract baseline if you are implementing a review queue or API.
- Start with bug fix or feature implementation if you want a realistic end-to-end supervision flow.
- Start with the report-only scenarios if you need stakeholder-readable examples for a particular engineering risk class.
