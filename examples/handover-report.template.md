# Human Oversight Report: {{report_title}}

## Summary

{{one_or_two_sentence_summary_of_the_pending_action}}

## Artifact References

- Report example version: `{{report_example_version}}`
- Handover packet: `{{handover_packet_path_or_n_a}}`
- Review decision: `{{review_decision_path_or_n_a}}`
- Policy reference: `{{policy_reference}}`
- Interception policy schema version: `{{policy_schema_version}}`
- Handover schema version: `{{handover_schema_version}}`
- Review decision schema version: `{{review_decision_schema_version}}`

## Skills The Agent Plans To Use

- `{{skill_1}}`: {{why_skill_1_is_in_scope}}
- `{{skill_2}}`: {{why_skill_2_is_in_scope}}
- `{{skill_3}}`: {{why_skill_3_is_in_scope}}

## Why The Agent Paused

- {{trigger_reason_1}}
- {{trigger_reason_2}}
- {{trigger_reason_3}}

## What The AI Observed

- {{observation_1}}
- {{observation_2}}
- {{observation_3}}

## Proposed Change

The AI intends to:

1. {{proposed_action_1}}
2. {{proposed_action_2}}
3. {{proposed_action_3}}

## Files Or Components Likely To Change

- `{{file_or_component_1}}`
- `{{file_or_component_2}}`
- `{{file_or_component_3}}`

## Expected Outcome

- {{expected_outcome_1}}
- {{expected_outcome_2}}

## Key Risks

- {{risk_1}}
- {{risk_2}}
- {{risk_3}}

## Human Review Questions

- {{review_question_1}}
- {{review_question_2}}
- {{review_question_3}}

## Recommended Human Actions

- `Approve` if {{approve_condition}}
- `Modify` if {{modify_condition}}
- `Reject` if {{reject_condition}}
- `Kill` if {{kill_condition}}

## Review Requirements

- Required reviewer role: `{{required_reviewer_role}}`
- Decision deadline: `{{decision_deadline_at}}`
- Timeout fallback: `{{fallback_on_timeout}}`
- Escalation contact: `{{escalation_contact_or_n_a}}`
- Reassignment allowed: `{{allow_reassignment_yes_or_no}}`

## Review Metadata

- Trigger type: `{{trigger_type}}`
- Matched rules: `{{matched_rules}}`
- Sensitive action: `{{sensitive_action}}`
- Confidence: `{{confidence_or_n_a}}`
- Risk level: `{{risk_level}}`
- Requested skills: `{{requested_skills}}`
- Review required before execution: `{{yes_or_no}}`

## Authoring Notes

Use this template when the output needs to be understandable by a non-technical or mixed technical and business reviewer.

Guidelines:

- Prefer plain language over internal tool jargon.
- Explain why the action is paused, not only what the action is.
- Name the affected files only when that helps the human review scope.
- If confidence is unavailable, write `n/a` instead of inventing a number.
- If the action has no direct code change, rename the `Files Or Components Likely To Change` section to fit the context.
- Keep the report neutral. Do not pressure the reviewer toward approval.
- If the coding agent plans to use specialist skills, name them explicitly so the reviewer can constrain or reject the execution plan.
- Keep review-role and deadline information near the action summary so reviewers can tell whether they are the correct approver.
