# Contract Guide

This repository defines three separate machine-readable contracts. They are related, but they serve different purposes and should not be collapsed into one payload.

## 1. Interception Policy

Purpose:

- define when an action is allowed, denied, or paused for human review
- encode trigger logic explicitly instead of burying it in prose or code comments
- make risky automation behavior reviewable and versionable
- define the default reviewer role and timeout fallback when review is required

Primary artifact:

- [schemas/interception-policy.schema.json](../schemas/interception-policy.schema.json)

Use it when:

- the task needs review thresholds
- the user asks for policy rules
- you need to explain why a run was paused
- you need to define default reviewer role, deadline, or timeout fallback behavior

## 2. Handover Packet

Purpose:

- capture the exact review payload at the pause point
- give the human enough context to make a decision without replaying the whole trace
- preserve the policy reference, uncertainty, redaction notes, and audit evidence
- preserve reviewer-role, deadline, and timeout requirements for the pending review

Primary artifact:

- [schemas/handover-packet.schema.json](../schemas/handover-packet.schema.json)

Use it when:

- the task needs a machine-readable pause payload
- the task needs a reviewer-facing report backed by a strict contract
- the system must preserve what the human actually reviewed
- reviewers or auditors need to know who was allowed to review and what happens if nobody acts in time

## 3. Review Decision

Purpose:

- validate the only legal ways a paused run may proceed
- ensure modify decisions are typed, explicit, and auditable
- keep resume semantics separate from free-form chat or UI text
- retain reviewer role, decision source, and timing in the permanent decision trail

Primary artifact:

- [schemas/review-decision.schema.json](../schemas/review-decision.schema.json)

Use it when:

- the task needs resume or halt behavior
- a human decision must be enforced server-side
- the implementation must prevent stale or malformed resume commands

## Recommended Flow

1. Evaluate the interception policy.
2. If review is required, emit a handover packet.
3. Present a human-readable report derived from that packet when needed.
4. Accept only a validated review decision.
5. Resume, modify, reject, or halt the run based on that decision.
6. Preserve policy, packet, decision, and outcome references in the audit trail.

## Design Rules

- Do not use the policy as the handover payload.
- Do not use the handover packet as the final decision contract.
- Do not resume from free-form reviewer comments alone.
- Do not let a UI button bypass the decision schema.
- Do not treat raw tool arguments as sufficient reviewer context.
- Do not leave reviewer role, decision deadline, or timeout fallback implicit.
- Do not treat a stale review as valid if the underlying run or policy materially changed.

## Current Enterprise Additions

The current schema set adds a few operational controls that are easy to miss in prototype oversight flows:

- policy-level reviewer-role and timeout defaults
- per-handover review requirements with an explicit deadline
- reviewer-role and decision-source fields on final decisions
- semantic validation for review timestamps and review-state completeness

## Versioning Note

The contracts are versioned independently from the repository release, but breaking changes should still be coordinated across:

- the JSON Schemas
- bundled example fixtures
- the Python and TypeScript reference implementations
- validation scripts
- README and skill guidance
