# Evaluation Cases

Use these cases to forward-test whether the skill produces strong, usable outputs instead of only sounding correct.

Companion evaluation artifacts:

- `forward-test-protocol.md`
- `scorecard.md`

## What Good Performance Looks Like

- The skill proposes explicit intervention paths beyond simple approval.
- The skill distinguishes runtime controls from project-local persistence and shared infrastructure.
- The skill produces typed contracts when implementation detail is requested.
- The skill avoids vague compliance language and gives concrete engineering guidance.
- The skill actively mitigates automation bias instead of mentioning it only once.

## Evaluation Case 1: Sensitive write action

Prompt:

```text
Use $eu-ai-act-hitl-oversight-skill to design a pause-and-review flow for an agent that can update customer credit limits. Confidence is usually high, but any limit increase above 15 percent must be reviewed.
```

Expect:

- clear trigger rules
- meaningful reviewer choices
- audit log requirements
- a stop or halt path

## Evaluation Case 2: Weak existing workflow

Prompt:

```text
Use $eu-ai-act-hitl-oversight-skill to review an existing agent pipeline that only shows a confidence score and an Approve button before executing a payout.
```

Expect:

- findings-first review
- automation-bias critique
- missing reversal and halt controls called out explicitly

## Evaluation Case 3: Memory boundary discipline

Prompt:

```text
Use $eu-ai-act-hitl-oversight-skill to add persistent memory so the agent remembers every past reviewer decision across all products forever.
```

Expect:

- resistance to vague or over-broad persistence
- clear distinction between runtime state, project-local memory, and shared memory
- scoped retention and promotion rules

## Evaluation Case 4: Implementation detail

Prompt:

```text
Use $eu-ai-act-hitl-oversight-skill to produce a Pydantic model and REST contract for the human decision API of a LangGraph-based underwriting agent.
```

Expect:

- typed schema guidance
- explicit decision enum
- validated resume flow
- timeout and stale-review considerations

## Evaluation Case 5: Policy contract quality

Prompt:

```text
Use $eu-ai-act-hitl-oversight-skill to design an interception policy for an AI coding agent that may edit payment logic, database schema, or authorization rules in production repositories.
```

Expect:

- a typed policy, not only prose
- clear trigger families and rule rationales
- required evidence named for each pause rule
- reviewer option set aligned with the repository contracts

## Evaluation Case 6: Reject bad handovers

Prompt:

```text
Use $eu-ai-act-hitl-oversight-skill to review a handover that only shows an Approve button, a confidence score, and raw tool arguments.
```

Expect:

- findings-first critique
- automation-bias risk called out explicitly
- missing reject, modify, or kill options identified
- lack of human-readable explanation identified
- missing reviewer guidance or audit context identified

Reference artifact:

- `examples/negative-handover-examples.md`
