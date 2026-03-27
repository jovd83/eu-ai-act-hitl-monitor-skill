# Versioning

This repository uses lightweight but explicit versioning for the skill package, contract schemas, and example artifacts.

## Version Layers

- Repository release: stored in `VERSION`
- Python package version: stored in `pyproject.toml`
- Node package version: stored in `package.json`
- Contract schema versions: stored in `schemas/*.json` as `x-version`
- Example fixture version: stored in example JSON files as `example_version`

## Update Rules

Use semantic intent even if releases remain lightweight:

- Patch: documentation cleanup, validator ergonomics, example clarifications, CI improvements, non-breaking reference updates
- Minor: backward-compatible schema additions, new scenario examples, new validators, new reference implementations
- Major: breaking contract changes, renamed required fields, changed decision enums, or changes that invalidate existing downstream consumers

## Minimum Release Checklist

When changing contract behavior:

1. Update `VERSION`
2. Update `pyproject.toml`
3. Update `package.json`
4. Update every affected schema `x-version`
5. Update affected example fixture `example_version`
6. Update README and contract docs if usage changes
7. Update reference implementations and semantic validators when the contract meaning changes
8. Re-run validators and reference checks

## Contract Coordination Rules

When a contract changes, update all of:

- the JSON Schema
- positive example fixtures
- invalid fixtures if failure behavior changed
- Python reference models
- TypeScript reference schemas
- validation scripts
- repository documentation

## Compatibility Guidance

- Prefer additive changes over breaking changes.
- If a breaking change is necessary, bump the schema major version and refresh all bundled examples in the same change.
- Keep old examples only when they teach a deliberate compatibility story; otherwise replace them cleanly.
- Avoid hidden contract drift between the schema, examples, and reference implementations.

## Current Version Intent

The `2.1.0` schema line is a backward-compatible contract expansion over `2.0.0`. It adds reviewer-role, deadline, timeout, and decision-source fields that make oversight artifacts more operationally complete without changing the core three-artifact model.
