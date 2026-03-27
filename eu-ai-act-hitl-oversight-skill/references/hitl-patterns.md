# HITL Patterns

Use this file when designing pause, review, modify, reject, or resume behavior.

## Preferred reference path: LangGraph

Primary sources:
- LangGraph human-in-the-loop docs: https://docs.langchain.com/oss/python/langgraph/human-in-the-loop
- LangChain human-in-the-loop middleware docs: https://docs.langchain.com/oss/python/langchain/human-in-the-loop
- LangGraph JS concept docs: https://langchain-ai.lang.chat/langgraphjs/concepts/human_in_the_loop/

Why this is the default path:

- It has a first-class interrupt mechanism
- It persists graph state for later resume
- It maps cleanly to approval, edit, and reject checkpoints

Implementation pattern:

1. Detect a trigger before a sensitive tool or decision is executed.
2. Build a structured handover packet.
3. Call the framework's interrupt or equivalent pause primitive.
4. Store the checkpoint key, trace ID, and review payload.
5. Wait for human input through UI, API, or webhook.
6. Validate the decision payload.
7. Resume with a typed command that routes to approve, modify, reject, or halt behavior.

Avoid:

- Busy waiting inside the agent process
- Resuming from unvalidated free-form text
- Pausing without persisting correlation IDs and state identifiers
- Treating the UI click as sufficient without a server-side decision contract

## Alternative pattern: framework-neutral supervisor wrapper

If the target framework lacks native interrupts:

- Wrap sensitive actions in a policy gateway
- Persist the pending action plus state snapshot in durable storage
- Mark the run as `paused-awaiting-human`
- Resume only through a review API that rehydrates the state and records the decision

This is less elegant than native checkpointing but still acceptable when carefully designed.

## Notes for AutoGen-style stacks

Look for the framework's supported human input or approval modes before inventing a custom flow. The key requirement is the same: durable pause, structured review payload, validated response, and explicit resume or halt semantics.

If the stack exposes only conversational human prompts, add a policy wrapper so the human decision is still stored as structured data rather than as an untyped chat message.

## Decision handling checklist

Make the reviewer action explicit:

- Validate the incoming decision against a strict schema.
- Require rationale for reject, kill, and modify decisions.
- Record the exact reviewed payload version.
- Prevent stale resume actions after the underlying run has materially changed.
- Define timeout and abandonment behavior up front.
