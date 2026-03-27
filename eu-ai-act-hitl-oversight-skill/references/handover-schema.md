# Handover Schema

Use this file when you need a strict contract for the policy, pause payload, or human decision API.

## Validation Guidance

Prefer:

- `Pydantic` for Python: https://docs.pydantic.dev/
- `Zod` for TypeScript: https://zod.dev/

Keep the contracts explicit and versioned. Do not pass raw dictionaries or unvalidated JSON between the agent runtime and the human review surface.

Machine-readable contracts:

- [../../schemas/interception-policy.schema.json](../../schemas/interception-policy.schema.json)
- [../../schemas/handover-packet.schema.json](../../schemas/handover-packet.schema.json)
- [../../schemas/review-decision.schema.json](../../schemas/review-decision.schema.json)

## Recommended Contract Split

Use three artifacts, not one:

1. `interception policy`: why review is required
2. `handover packet`: what the human sees at the pause point
3. `review decision`: how the run is allowed to continue, change, or stop

## Suggested Handover Shape

```json
{
  "handover_id": "uuid",
  "created_at": "2026-03-25T19:00:00Z",
  "trace_id": "otel-trace-id",
  "run_id": "agent-run-id",
  "agent": {
    "name": "orchestrator",
    "version": "1.4.2",
    "policy_version": "2026-03-25"
  },
  "policy": {
    "policy_id": "claims-policy-v2",
    "policy_version": "2026-03-25",
    "policy_reference": "policies/claims-policy-v2.json",
    "review_required": true
  },
  "trigger": {
    "type": "low_confidence",
    "matched_rules": [
      "confidence_below_0_85",
      "update_database_requires_review"
    ],
    "confidence": 0.73,
    "risk_level": "medium"
  },
  "pending_action": {
    "summary": "Update a customer billing record",
    "tool_name": "update_database",
    "tool_args_redacted": {
      "customer_id": "cust_123",
      "status": "past_due"
    },
    "side_effects": [
      "writes customer status"
    ],
    "affected_resources": [
      "billing ledger"
    ]
  },
  "explanation": {
    "goal": "Mark the account as past due after failed payment verification",
    "why_now": "The upstream payment check returned a failure code",
    "evidence_summary": [
      "Payment verification API returned status failed",
      "Customer has two unpaid invoices"
    ],
    "reasoning_summary": "The agent selected the standard collections workflow but confidence dropped because invoice data and payment metadata disagree.",
    "uncertainty_summary": "The likely action is clear, but the conflicting upstream records make blind approval unsafe.",
    "known_risks": [
      "Incorrect status update could trigger collections outreach",
      "Source systems may be out of sync"
    ]
  },
  "review_guidance": {
    "questions": [
      "Should the status update proceed now?",
      "Should the account be routed to manual review instead?"
    ],
    "recommended_actions": [
      "Approve only if the conflicting evidence is understood and acceptable",
      "Modify if the status should be changed to manual review",
      "Reject or kill if the action should not continue"
    ]
  },
  "human_options": [
    "approve",
    "modify",
    "reject",
    "kill",
    "request_more_context"
  ],
  "audit": {
    "review_payload_version": "2.1.0",
    "redaction_notes": [
      "Reviewer packet omits full billing records."
    ],
    "evidence_refs": [
      "trace:trace-123",
      "policy:claims-policy-v2"
    ]
  },
  "review": {
    "status": "pending",
    "reviewer_id": null,
    "review_started_at": null,
    "review_submitted_at": null,
    "review_duration_ms": null,
    "decision_reason": null,
    "modifications": null
  }
}
```

## Decision Contract

Use a closed enum for decisions:

- `approve`
- `modify`
- `reject`
- `kill`
- `request_more_context`

For `modify`, require:

- the approved replacement action
- changed fields
- replacement arguments
- whether the original action remains blocked

Do not use a free-form note as the authoritative resume signal.

## Resume State Machine

Use an explicit state machine:

- `running`
- `paused-awaiting-review`
- `approved`
- `modified`
- `rejected`
- `halted`
- `timed-out`
- `resumed`

`timeout` belongs in runtime or review status, not in the human decision enum.

Never infer the next state from a free-form text comment alone.
