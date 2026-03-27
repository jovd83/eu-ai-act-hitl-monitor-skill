# Contributing

Thanks for improving this repository.

## Contribution Bar

Contribute only changes that make the skill:

- clearer to invoke
- safer to use
- easier to validate
- easier to install
- easier to extend without contract drift

Avoid speculative additions such as large framework scaffolds, placeholder services, or product features that are not implemented in this repository.

## Before You Edit

Read these files first:

- [eu-ai-act-hitl-oversight-skill/SKILL.md](./eu-ai-act-hitl-oversight-skill/SKILL.md)
- [docs/contracts.md](./docs/contracts.md)
- [docs/versioning.md](./docs/versioning.md)
- [examples/README.md](./examples/README.md)

The repository is designed so the skill contract, schemas, examples, validators, and reference implementations move together.

## Repository Principles

- Keep runtime execution concerns separate from repository-local artifacts.
- Keep shared-memory concerns out of this repository unless an explicit integration boundary is being added.
- Prefer explicit typed contracts over prose-only guidance.
- Favor narrow, auditable changes over clever abstractions.
- Keep the skill, schemas, examples, validators, and reference implementations aligned.
- Prefer additive, reviewable improvements over speculative abstractions.
- Preserve the distinction between conceptual integrations and implemented repository contents.

## If You Change One Layer, Check The Adjacent Layers

Update adjacent artifacts when you materially change:

- [eu-ai-act-hitl-oversight-skill/SKILL.md](./eu-ai-act-hitl-oversight-skill/SKILL.md)
- [schemas](./schemas)
- [examples](./examples)
- [reference-implementations](./reference-implementations)
- [scripts](./scripts)
- [README.md](./README.md)
- [docs/versioning.md](./docs/versioning.md)

Contract changes are not finished until the examples, validators, and reference implementations match.

## Local Validation

Run these before proposing a change:

```powershell
python .\scripts\validate_repo.py
```

If you are working on a single layer, you can still run the narrower validators directly from `scripts/`.

## Style Expectations

- Prefer short, precise, production-grade language.
- Keep examples realistic and risk-aware.
- Do not claim legal compliance where the repository only provides technical guidance.
- Do not expose hidden reasoning, secrets, or unnecessary personal data in examples.
- Label conceptual or optional components clearly when they are not implemented here.
- Keep reviewer-facing examples neutral and decision-capable.
- Preserve the explicit three-layer memory model unless the change is intentionally about that boundary.

## Pull Request Checklist

- The skill still validates.
- All positive example fixtures still validate.
- Invalid fixtures still fail for the intended reasons.
- Version markers are updated when schema or contract behavior changes.
- README, schema, examples, and reference implementations remain consistent.
- Any new persistence or memory behavior is explicitly scoped.
- Any new integration is clearly labeled as implemented or conceptual.
- Any new reviewer-role, deadline, or timeout behavior is reflected in examples and semantic validators.
