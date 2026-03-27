# Changelog

## 1.1.0 - 2026-03-27

- rewrote the core skill contract to be more explicit about intake, deliverable modes, response contracts, timeout handling, and architectural boundaries
- aligned the repository more tightly with the current Agent Skills format, including compatibility metadata and stronger skill validation rules
- upgraded the contract model to version `2.1.0` with reviewer-role, deadline, timeout, and decision-source fields
- strengthened semantic validation for review timestamps and review-state completeness
- added a top-level `validate_repo.py` workflow for faster local validation and cleaner contributor experience
- refreshed README, contract docs, example catalog, and reviewer-facing templates to match the stronger operating model

## 1.0.0 - 2026-03-27

- promoted the repository from a prototype-style skill package to a versioned, contract-driven release
- added a first-class interception policy schema and validator
- upgraded the handover packet and review decision contracts to carry explicit policy, reviewer guidance, and audit metadata
- refreshed all positive and negative example fixtures to match the stronger contracts
- strengthened the Python and TypeScript reference implementations
- improved repository validation with shared helpers and a bundled example-validation runner
- rewrote the main documentation to make installation, contracts, validation, and operating boundaries easier to understand
