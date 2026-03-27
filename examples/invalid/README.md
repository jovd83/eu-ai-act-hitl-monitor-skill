# Invalid Validation Fixtures

Use these fixtures to confirm the repository validators fail for the right reasons.

Included cases:

- `invalid-handover-missing-review-status.json`: missing required `review.status`
- `invalid-handover-bad-trigger-type.json`: invalid `trigger.type` enum value
- `invalid-handover-pending-review-fields-populated.json`: semantically invalid pending review state with populated reviewer fields
- `invalid-review-bad-timestamp.json`: malformed review timestamp
- `invalid-review-submitted-before-start.json`: review submission time earlier than review start
- `invalid-review-extra-field.json`: unexpected extra field in the decision payload
- `invalid-policy-missing-human-options.json`: pause-for-review policy rule without the required human option set

These files are intentionally invalid and should not be used as implementation examples.
