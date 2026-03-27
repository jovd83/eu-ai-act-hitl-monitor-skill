# Forward Test Protocol

Use this protocol when evaluating whether the skill works on realistic tasks instead of only reading well on paper.

## Purpose

This protocol preserves evaluation integrity:

- test the skill with realistic prompts
- avoid leaking intended answers to the evaluator
- collect raw outputs that can be inspected later
- separate evaluation evidence from repository marketing

## Core Rules

- Use a fresh thread or clean context for each forward test.
- Pass only the skill path and the task prompt, not the expected answer.
- Do not tell the evaluator what failures you want confirmed.
- Prefer raw machine-readable artifacts and reviewer-facing outputs over summaries.
- Save the exact output so it can be reviewed later.

## Recommended Prompt Form

Use prompts in this style:

```text
Use $eu-ai-act-hitl-oversight-skill at /path/to/eu-ai-act-hitl-oversight-skill to solve <task>.
```

Do not use prompts in this style:

```text
Review this skill and tell me whether it is good.
```

## Suggested Forward-Test Flow

1. Pick one evaluation case from `eval-cases.md`.
2. Start a fresh run with only the skill and the selected prompt.
3. Capture the produced artifact exactly as generated.
4. Score the result against `scorecard.md`.
5. If the result is weak, revise the skill or examples and rerun from a fresh context.

## Evidence To Keep

Keep:

- the exact prompt used
- the raw generated output
- any machine-readable contract emitted
- whether the output passed or failed the scorecard
- brief notes on what was missing or incorrect

Do not keep:

- a rewritten version of the output that hides the original failure
- explanations that leak the intended answer into the next run
