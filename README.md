# EU AI Act HITL Oversight Skill

Enterprise-grade Agent Skill for designing, reviewing, and retrofitting human oversight around higher-risk agent actions.

This repository helps turn risky agent behavior into a reviewable operating model with clear pause triggers, reviewer handovers, decision contracts, timeout handling, and audit evidence. It is designed for AI platform teams, product architects, security-minded maintainers, and engineers who need stronger control boundaries than "show a confidence score and ask for approval."

## Why This Repository Exists

Most oversight guidance stops at principles. This repository is built for implementation:

- a triggerable skill contract in [`eu-ai-act-hitl-oversight-skill/SKILL.md`](./eu-ai-act-hitl-oversight-skill/SKILL.md)
- repository-backed references for legal grounding and runtime patterns
- typed JSON Schemas for policy, handover, and human decision handling
- Python and TypeScript reference implementations
- positive and negative fixtures
- local validators and CI automation
- forward-test evaluation guidance

## What The Skill Does

Use this skill when you need to:

- decide which agent actions must pause for human review
- replace approval-only flows with real reviewer choice
- produce a human-readable handover and a machine-readable review packet
- define strict resume, modify, reject, kill, and request-more-context behavior
- preserve enough evidence for audit, incident review, or post-hoc investigation
- critique an unsafe existing workflow with findings first

The skill is responsible for the supervisory layer only. It does not classify legal scope on its own, replace legal counsel, or ship a production review service, queue, UI, or persistence backend.

## Standards Alignment

This repository is intentionally aligned with the current open Agent Skills format:

- the skill lives in a single skill directory with a `SKILL.md` entrypoint
- frontmatter uses Agent Skills compatible fields and naming constraints
- Codex-facing UI metadata is kept in `agents/openai.yaml`
- detailed material is pushed into `references/` to preserve progressive disclosure
- repository-local validation checks both skill-shape rules and contract integrity

Use the bundled validators for local assurance, and optionally run an external Agent Skills validator if your publishing flow requires it.

## Quick Start

### 1. Install the skill

Copy the `eu-ai-act-hitl-oversight-skill` folder into your local skills directory.

Typical locations:

- Windows: `%USERPROFILE%\\.codex\\skills`
- Cross-platform fallback: `$CODEX_HOME/skills`

### 2. Validate the repository

```powershell
python .\scripts\validate_repo.py
```

This runs skill-shape validation, version checks, positive and negative fixture validation, Python reference-model loading, and Node.js typechecking when `npm` is available.

### 3. Invoke the skill

```text
Use $eu-ai-act-hitl-oversight-skill to design or review the interception policy, reviewer handover, review-decision contract, timeout behavior, and audit trail for this agent system.
```

## Output Modes

The skill should prefer concrete artifacts over essay-style output.

### Findings-first review

- missing controls
- automation-bias risks
- contract gaps
- risky defaults
- recommended fixes in priority order

### Architecture package

- runtime control boundaries
- pause, timeout, and escalation flow
- state transitions
- persistence and audit assumptions

### Contract package

- interception policy
- handover packet
- review decision payload
- validation and replay-safety rules

### Reviewer package

- a readable markdown handover
- reviewer role, deadline, and timeout fallback
- the matching machine-readable packet when implementation detail is required

### Implementation package

- stack-aligned code or pseudocode
- review API contract
- schema or model definitions
- redaction and logging requirements

## Contract System

This repository treats oversight as three separate contracts. They are related, but they serve different responsibilities and should not be collapsed together.

### 1. Interception policy

Defines when an action is allowed, denied, or paused for human review.

- schema: [schemas/interception-policy.schema.json](./schemas/interception-policy.schema.json)
- example: [examples/interception-policy.example.json](./examples/interception-policy.example.json)
- validator: `python .\scripts\validate_interception_policy.py .\examples\interception-policy.example.json`

### 2. Handover packet

Defines what the reviewer sees at the pause point, including reviewer-role and timeout requirements.

- schema: [schemas/handover-packet.schema.json](./schemas/handover-packet.schema.json)
- example: [examples/handover-packet.example.json](./examples/handover-packet.example.json)
- validator: `python .\scripts\validate_handover_packet.py .\examples\handover-packet.example.json`

### 3. Review decision

Defines the only legal ways a paused run may continue, change, reject, or halt.

- schema: [schemas/review-decision.schema.json](./schemas/review-decision.schema.json)
- example: [examples/review-decision.example.json](./examples/review-decision.example.json)
- validator: `python .\scripts\validate_review_decision.py .\examples\review-decision.example.json`

Current versions:

- repository release: `1.1.0`
- schema set: `2.1.0`
- example fixture set: `2.1.0`

See [docs/contracts.md](./docs/contracts.md) for the operating relationship between these artifacts.

## Memory And Architectural Boundaries

This skill uses an explicit three-layer memory model:

- Runtime memory: active run state, trace context, evidence summary, and pending review payload for the current execution only.
- Project or skill memory: versioned schemas, examples, validators, and reference docs stored in this repository.
- Shared memory: optional external infrastructure for stable cross-agent knowledge. This repository does not implement it directly.

Promotion rules:

- do not automatically persist runtime state
- do not automatically promote project-local patterns into shared memory
- promote only stable, auditable, and appropriately scoped knowledge

Keep these concerns separate from runtime execution. This repository is not a queue processor, workflow engine, or shared-memory service.

## Validation And Evaluation

Validation layers:

- skill structure and metadata validation
- contract validation for policy, handover, and decision JSON
- negative-fixture checks for expected failure modes
- semantic timestamp and review-state checks beyond raw schema validation
- Python reference-model validation with Pydantic
- TypeScript typechecking for the Zod reference contracts
- version-consistency checks across release markers and examples

Evaluation guidance lives in:

- [evals/eval-cases.md](./evals/eval-cases.md)
- [evals/forward-test-protocol.md](./evals/forward-test-protocol.md)
- [evals/scorecard.md](./evals/scorecard.md)

The quality bar is not whether the skill sounds compliant. It is whether it produces usable, risk-aware, implementation-ready artifacts with clean runtime boundaries.

## Repository Layout

```text
.
|-- README.md
|-- CHANGELOG.md
|-- VERSION
|-- eu-ai-act-hitl-oversight-skill/
|   |-- SKILL.md
|   |-- agents/openai.yaml
|   `-- references/
|-- schemas/
|   |-- interception-policy.schema.json
|   |-- handover-packet.schema.json
|   `-- review-decision.schema.json
|-- reference-implementations/
|   |-- python/handover_models.py
|   `-- typescript/handoverSchema.ts
|-- scripts/
|   |-- validate_repo.py
|   |-- validate_skill.py
|   |-- validate_interception_policy.py
|   |-- validate_handover_packet.py
|   |-- validate_review_decision.py
|   |-- validate_examples.py
|   `-- validate_versions.py
|-- examples/
|   |-- README.md
|   |-- example-prompts.md
|   |-- handover-report.template.md
|   |-- interception-policy.example.json
|   |-- handover-packet.example.json
|   |-- review-decision.example.json
|   `-- invalid/
|-- docs/
|   |-- contracts.md
|   `-- versioning.md
`-- evals/
    |-- eval-cases.md
    |-- forward-test-protocol.md
    `-- scorecard.md
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Out Of Scope

Future additions may be useful, but they are intentionally not implemented here:

- production reviewer UI
- queue processor or webhook server
- hosted persistence layer
- policy execution engine package
- legal opinion content

The repository is intentionally focused on a high-quality skill contract, typed artifacts, and a validation-first maintainer experience.
