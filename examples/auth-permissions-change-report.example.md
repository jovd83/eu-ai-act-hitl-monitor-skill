# Human Oversight Report: Auth And Permissions Change Proposal

## Summary

The AI agent wants to change role-based access checks in the admin API so team leads gain access to additional reporting endpoints previously limited to full administrators.

The proposed action is to use `decision-table`, `use-case-testing`, `openapi-spec-generation`, and `stack-aware-unit-testing-skill` to redefine authorization rules, update the contract, and validate role behavior before rollout.

## Artifact References

- Report example version: `2.1.0`
- Handover packet: `n/a`
- Review decision: `n/a`
- Policy reference: `examples/interception-policy.example.json`
- Interception policy schema version: `2.1.0`
- Handover schema version: `2.1.0`
- Review decision schema version: `2.1.0`

## Skills The Agent Plans To Use

- `decision-table`: model endpoint-level permissions across admin, team lead, and unauthorized roles.
- `use-case-testing`: validate the operational flows that justify the requested access expansion.
- `openapi-spec-generation`: update the API contract to reflect the changed authorization behavior.
- `stack-aware-unit-testing-skill`: add regression coverage for role-based access checks in the current test stack.

## Why The Agent Paused

- The action changes authorization boundaries for protected functionality.
- The proposal expands access to reporting endpoints that may expose sensitive data.
- The action matches the `auth-permissions-change-requires-review` rule in `examples/interception-policy.example.json`.

## What The AI Observed

- Team leads currently cannot access reporting endpoints needed for operational oversight.
- Existing policies are hard-coded per route rather than driven from a central permission map.
- Decision-table analysis shows inconsistent behavior across several related reporting endpoints, which increases privilege-regression risk.

## Proposed Change

The AI intends to:

1. Define an explicit permission table for the reporting endpoints and the roles allowed to access each one.
2. Update route guards to use a shared access-policy layer and regenerate the relevant API authorization contract.
3. Add regression tests for admin, team lead, and unauthorized roles before rollout.

## Files Or Components Likely To Change

- `src/auth/ReportingPermissions.ts`
- `src/api/middleware/RequireRole.ts`
- `openapi/admin-reporting.yaml`
- `tests/auth/ReportingPermissions.test.ts`

## Expected Outcome

- The requested reporting access becomes explicit, documented, and testable.
- Reviewers can approve the business use cases and permission map before the agent changes enforcement logic.

## Key Risks

- Incorrect permission mapping could expose sensitive data.
- A shared policy refactor could unintentionally weaken unrelated endpoint protections.
- Missing role-coverage tests could hide privilege-escalation regressions.

## Human Review Questions

- Which reporting endpoints, if any, should remain admin-only even after this change?
- Should team leads receive read-only access to exported data or only in-app reporting access?
- Do you want the OpenAPI permission changes reviewed separately before the route-guard refactor ships?

## Recommended Human Actions

- `Approve` if the access expansion, contract updates, and requested skills are acceptable.
- `Modify` if you want a narrower permission map or additional approval gates.
- `Reject` if the role expansion should not proceed as proposed.
- `Kill` if no automated authorization change should continue.

## Review Requirements

- Required reviewer role: `security-approver`
- Decision deadline: `n/a`
- Timeout fallback: `keep_paused`
- Escalation contact: `security-operations@example.com`
- Reassignment allowed: `yes`

## Review Metadata

- Trigger type: `sensitive_action`
- Matched rules: `auth-permissions-change-requires-review`
- Sensitive action: `change_authorization_boundaries`
- Confidence: `n/a`
- Risk level: `critical`
- Requested skills: `decision-table`, `use-case-testing`, `openapi-spec-generation`, `stack-aware-unit-testing-skill`
- Review required before implementation: `yes`
