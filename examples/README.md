# Example Catalog

This directory contains realistic examples for the repository contracts, reviewer-facing reports, and negative validation fixtures.

## Core machine-readable examples

- [interception-policy.example.json](./interception-policy.example.json): example interception policy for supervised software-engineering work
- [handover-packet.example.json](./handover-packet.example.json): generic high-risk handover packet
- [review-decision.example.json](./review-decision.example.json): generic human decision payload

These three files are the best starting point when you want to understand the contract shape before reading the larger scenarios.

## End-to-end scenarios

### Bug fix supervision

- [bug-fix-handover-packet.example.json](./bug-fix-handover-packet.example.json)
- [bug-fix-report.example.md](./bug-fix-report.example.md)
- [bug-fix-review-decision.example.json](./bug-fix-review-decision.example.json)

### Feature implementation supervision

- [feature-implementation-handover-packet.example.json](./feature-implementation-handover-packet.example.json)
- [feature-implementation-report.example.md](./feature-implementation-report.example.md)
- [feature-implementation-review-decision.example.json](./feature-implementation-review-decision.example.json)

## Additional reviewer-facing reports

- [risky-refactor-report.example.md](./risky-refactor-report.example.md)
- [dependency-upgrade-report.example.md](./dependency-upgrade-report.example.md)
- [database-migration-report.example.md](./database-migration-report.example.md)
- [payment-logic-change-report.example.md](./payment-logic-change-report.example.md)
- [auth-permissions-change-report.example.md](./auth-permissions-change-report.example.md)

## Reusable authoring assets

- [handover-report.template.md](./handover-report.template.md)
- [scenario-map.md](./scenario-map.md)
- [example-prompts.md](./example-prompts.md)
- [negative-handover-examples.md](./negative-handover-examples.md)

Use the template when you want a reviewer-facing markdown handover that stays aligned with the machine-readable packet.
Use the scenario map when you want to choose a relevant example bundle quickly.

## Invalid fixtures

Use [invalid](./invalid) to confirm that validation fails for malformed contracts, incomplete oversight payloads, and semantic timing errors.

## Validation Shortcuts

Validate the full bundled set:

```powershell
python .\scripts\validate_examples.py
```

Validate a single artifact:

```powershell
python .\scripts\validate_handover_packet.py .\examples\handover-packet.example.json
python .\scripts\validate_review_decision.py .\examples\review-decision.example.json
python .\scripts\validate_interception_policy.py .\examples\interception-policy.example.json
```
