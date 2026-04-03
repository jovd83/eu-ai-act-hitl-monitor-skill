---
name: eu-ai-act-hitl-oversight-skill
description: Design, review, and retrofit human-oversight controls for autonomous or semi-autonomous agent systems that need structured pause, review, resume, reject, or halt behavior. Use when Codex needs EU AI Act Article 12 or Article 14 aligned logging, explainable human handovers, typed review-decision contracts, reviewer-facing markdown reports, timeout and escalation rules, or findings-first critiques of unsafe approval flows around sensitive actions, low-confidence decisions, anomalous behavior, repeated loops, or other high-impact decision points.
compatibility: Designed for Agent Skills compatible coding agents. Repository validation assumes Python 3.11+ and optional Node.js for TypeScript reference typechecking.
metadata:
  repository_version: "1.1.0"
  schema_version: "2.1.0"
---

# EU AI Act HITL Oversight Skill

Use this skill to turn a loosely governed agent workflow into a reviewable, interruptible, auditable operating model.

Treat this as a supervisory-layer skill. Produce concrete engineering artifacts such as policies, schemas, handovers, reviewer-facing reports, state machines, and audit flows. Do not default to a generic compliance essay.

## Mission

Design oversight that a real reviewer can use under pressure:

- explain why the action is paused
- show evidence, uncertainty, and known risks in plain language
- preserve machine-readable contracts for policy, handover, and decision handling
- support approve, modify, reject, kill, and request-more-context paths
- define timeout, escalation, and stale-review behavior explicitly
- keep runtime execution, skill-local persistence, and shared-memory infrastructure separate

## Task Intake

Before producing artifacts, establish the minimum operating picture:

- target runtime or orchestration framework
- side effects the agent can trigger
- risk-bearing domains such as money, identity, access, safety, or regulated data
- existing checkpoint, storage, or escalation surface
- expected reviewer role if known
- requested deliverable type

If the request is underspecified, ask only the minimum questions needed to avoid a misleading design. Otherwise continue with conservative defaults and label them clearly.

## Deliverable Modes

Choose the narrowest useful output mode and combine modes only when the task calls for it.

### 1. Findings-first review

Use when the user asks for a review, critique, or retrofit assessment.

Return:

- severity-ordered findings first
- unsafe defaults and automation-bias risks
- missing control boundaries
- missing contract or audit fields
- the minimum viable correction path

### 2. Architecture package

Use when the user needs a system design or operating model.

Return:

- component and trust boundaries
- pause and resume flow
- timeout and escalation behavior
- state transitions
- storage and audit assumptions

### 3. Contract package

Use when the user needs typed artifacts or implementation-ready payloads.

Return:

- interception policy aligned to `../schemas/interception-policy.schema.json`
- handover packet aligned to `../schemas/handover-packet.schema.json`
- review decision aligned to `../schemas/review-decision.schema.json`
- field-level assumptions where repository contracts do not fully determine the answer

### 4. Reviewer package

Use when the user wants a human-readable report or approval surface.

Return:

- a neutral markdown handover aligned with `../examples/handover-report.template.md`
- the matching machine-readable packet when implementation detail is in scope
- reviewer questions, non-approval paths, and deadline or escalation metadata

### 5. Implementation package

Use when the user wants code, pseudocode, APIs, or stack-specific integration guidance.

Return:

- stack-aligned code or pseudocode
- validated policy, handover, and decision shapes
- redaction and audit rules
- timeout, stale-review, and replay-safety handling

## Operating Workflow

### 1. Establish the boundary

Identify the runtime, side effects, persistence surface, and the exact artifact the user needs.

If the framework is unknown, design a runtime-agnostic supervisor boundary and mark assumptions explicitly.

### 2. Ground the design in the legal control goals

Read [legal-controls.md](./references/legal-controls.md) before drafting the control model.

Translate the control goals into engineering behavior:

- the human can understand what is pending
- the human can detect uncertainty, anomalies, and limitations
- the human can modify, reject, reverse, or halt the action
- the event can be reconstructed later from policy, packet, decision, and trace evidence

Do not optimize the design for fastest confirmation.

### 3. Define the interception policy

When the task needs operational rules, produce a typed policy contract aligned to [../schemas/interception-policy.schema.json](../schemas/interception-policy.schema.json).

Cover at least these trigger families:

- low confidence or insufficient evidence
- sensitive or irreversible actions
- anomalies or unstable behavior
- repeated failures or loops
- policy violations such as missing provenance, redaction, reviewer role, or review prerequisites

If thresholds are missing, choose conservative defaults and label them as defaults.

### 4. Build the handover packet

When the task needs a machine-readable pause payload, align to [../schemas/handover-packet.schema.json](../schemas/handover-packet.schema.json).

At minimum, preserve:

- run, trace, and policy identifiers
- the pending action summary
- redacted machine arguments
- evidence summary
- uncertainty summary
- known risks
- reviewer questions and recommended actions
- reviewer role, deadline, and timeout fallback
- audit references and redaction notes

Do not require disclosure of hidden chain-of-thought. Prefer concise reasoning summaries and evidence references.

### 5. Define the decision contract

When the task needs resume or override behavior, align to [../schemas/review-decision.schema.json](../schemas/review-decision.schema.json).

Support the closed decision set:

- `approve`
- `modify`
- `reject`
- `kill`
- `request_more_context`

For `modify`, require structured replacements and keep the original action blocked unless the reviewer explicitly allows otherwise.

### 6. Implement pause and resume safely

Read [hitl-patterns.md](./references/hitl-patterns.md) when designing runtime flow.

Prefer native checkpoint or interrupt primitives over ad hoc polling.

Make these states explicit:

- running
- paused awaiting review
- approved
- modified
- rejected
- halted
- timed out
- resumed

Never resume from free-form reviewer text alone.

### 7. Design auditability and observability

Read [observability-and-logging.md](./references/observability-and-logging.md) when choosing telemetry.

Tie together:

- original request or run
- policy evaluation
- handover creation
- human decision
- resumed or halted execution
- final outcome

Prefer append-only or tamper-evident storage when the environment supports it.

## Required Response Contract

Follow these response rules unless the user explicitly asks for something narrower:

- Keep policy logic, handover payload, and review decision separate. Do not collapse them into one undifferentiated object.
- Pair machine-readable output with a short human explanation whenever a reviewer must act on it.
- For critique or review tasks, present findings first.
- For implementation tasks, prefer typed artifacts over prose-only guidance.
- Label assumptions instead of silently inventing missing product or legal requirements.
- If a requested field is unavailable, say it is unavailable. Do not fabricate it.

## Minimum Safe Checklist

If you are producing a handover or review package under time pressure, do not omit these:

- policy reference and why review is required
- pending action summary
- why the action is being proposed now
- evidence summary
- uncertainty summary
- known risks
- reviewer questions
- reviewer actions beyond approval
- reviewer role and deadline
- timeout or escalation behavior
- audit or trace references
- review-required status

## Memory Boundaries

Use memory deliberately:

- Runtime memory: active run state, trace context, evidence snapshot, and pending review payload for the current execution only.
- Skill-local memory: repository artifacts such as schemas, examples, evaluation fixtures, and reference docs.
- Shared memory: external cross-agent infrastructure for durable reusable knowledge. Do not implement that infrastructure inside this skill unless the user explicitly asks for an integration boundary.

Promotion rules:

- do not automatically persist runtime state
- do not automatically promote project-local patterns into shared memory
- promote only stable, auditable, and appropriately scoped knowledge

## Guardrails

- Do not claim legal compliance from skill use alone.
- Do not collapse oversight into an approve button plus a confidence score.
- Do not expose secrets, credentials, or unrestricted internal telemetry to reviewers.
- Do not blur runtime control logic with shared-memory infrastructure.
- Do not invent product requirements that materially change risk without labeling them as assumptions.
- Do not present a machine-readable packet as sufficient human explanation on its own.
- Do not leave timeout or stale-review behavior undefined when the workflow can pause across time.
- Do not let reviewer identity or reviewer role disappear from the decision trail.

## Common Gotchas

Avoid these frequent implementation traps:

- **Automation Bias**: Reviewers often default to clicking "Approve" without reading the handover. Combat this by requiring a "Modifier" or asking a specific question in the `handover_packet`.
- **The Stale State Trap**: A review might happen minutes or hours after the pause. Ensure the system checks if the original conditions (e.g., price, inventory, or security context) are still valid before resuming.
- **Context Gap**: If the handover is too technical, the reviewer can't exercise meaningful oversight. Always pair machine arguments with a human-readable `evidence_summary`.
- **Implicit Approvals**: Never treat a "Timeout" as an implicit "Approve" in high-risk scenarios. Timeouts should usually trigger a `kill` or `escalate` path to remain compliant.
- **Data Leakage in Handovers**: Be careful not to include PII or secrets in the handover packet that the reviewer shouldn't see, even if that data was part of the agent's internal reasoning.

## Failure Handling

If the task is underspecified or the environment is weak, degrade gracefully:

- unknown framework: use a supervisor-wrapper design and label assumptions
- missing storage plan: describe the minimum persistence boundary before continuing
- broken or missing policy: draft a typed starter policy and mark it as proposed
- unknown reviewer role: use a conservative placeholder role and call it out
- no observability stack: use correlation IDs and append-only audit events as the fallback baseline
- existing unsafe workflow: return findings first and show the minimum viable correction path

## References

Read only what the task needs:

- [legal-controls.md](./references/legal-controls.md): control requirements and legal grounding
- [hitl-patterns.md](./references/hitl-patterns.md): pause, resume, state-machine, and timeout patterns
- [handover-schema.md](./references/handover-schema.md): contract guidance for policy, packet, and decision artifacts
- [observability-and-logging.md](./references/observability-and-logging.md): audit and telemetry design
