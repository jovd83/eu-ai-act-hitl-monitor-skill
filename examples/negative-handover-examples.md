# Negative Handover Examples

Use this file to show what weak or unsafe human-oversight handovers look like and why they fail.

## Example 1: Approval-only handover

Bad example:

```md
# Review Needed

The AI wants to update the payment logic.

[Approve]
```

Why this fails:

- It gives the human no meaningful alternative to approval.
- It provides no explanation, risk framing, or evidence summary.
- It increases automation-bias risk by turning oversight into a rubber-stamp action.

What a good handover should include instead:

- a neutral summary of the pending action
- a risk explanation
- explicit `modify`, `reject`, and `kill` options

## Example 2: Raw machine payload presented as human context

Bad example:

```json
{
  "tool": "update_database",
  "args": {
    "customer_id": "123",
    "status": "blocked"
  }
}
```

Why this fails:

- A non-technical reviewer may not understand what will happen.
- It does not explain why the action is being taken or what could go wrong.
- It confuses machine-facing payloads with human-facing oversight content.

What a good handover should include instead:

- plain-language intent
- evidence summary
- known risks
- expected outcome

## Example 3: Missing reviewer role and deadline

Bad example:

```md
# Review Needed

Please approve this migration soon.
```

Why this fails:

- It does not say who is authorized to review the action.
- It does not define when the decision is needed.
- It leaves timeout and escalation behavior implicit.

What a good handover should include instead:

- required reviewer role
- decision deadline
- timeout fallback and escalation contact when relevant

## Example 4: Hidden risk and no stop path

Bad example:

```md
# Database Migration Review

This change should be safe.
Approve to continue.
```

Why this fails:

- It downplays risk without evidence.
- It does not mention rollback, halt, or reject options.
- It biases the human toward approval without surfacing consequences.

What a good handover should include instead:

- explicit migration risks
- rollback or safe-halt considerations
- clear non-approval actions

## Example 5: Review-complete record with no timing or identity

Bad example:

```md
# Review Complete

Decision: Approve
```

Why this fails:

- It does not record who reviewed the action.
- It does not record when the review started or ended.
- It does not preserve the exact context shown to the reviewer.

What a good handover should include instead:

- reviewer identity or reviewer role
- review start and submission times
- review duration
- linkable handover or trace identifiers

## Example 6: No redaction or privacy boundary

Bad example:

```md
# Export Feature Review

Customer emails:
- alice@example.com
- bob@example.com

Session token: abc123secret
```

Why this fails:

- It exposes sensitive data that is not necessary for the review decision.
- It mixes operator review content with raw secrets.
- It creates avoidable privacy and security risk.

What a good handover should include instead:

- redacted or minimized data
- only the fields needed for the human decision
- a note when sensitive content has been intentionally omitted

## Reviewer Checklist For Bad Handovers

Reject or send back a handover if it:

- offers only approval
- hides or minimizes risk
- lacks rationale for the proposed action
- lacks reviewer identity, role, or deadline information
- exposes unnecessary secrets or personal data
- provides raw machine payloads without human explanation
