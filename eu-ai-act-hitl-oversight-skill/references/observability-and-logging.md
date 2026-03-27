# Observability And Logging

Use this file when the task needs a trace model, audit design, or exportable evidence bundle.

## Preferred baseline

Primary sources:
- OpenTelemetry concepts: https://opentelemetry.io/docs/concepts/
- OpenTelemetry specification overview: https://opentelemetry.io/docs/reference/specification/overview/
- OpenTelemetry trace semantic conventions: https://opentelemetry.io/docs/specs/semconv/general/trace/

Treat the handover as a traceable event, not a detached log line.

Minimum telemetry model:

- One trace per user request or orchestrated run
- Spans for planning, tool calls, policy evaluation, handover creation, human review, and resumed execution
- Shared trace or correlation IDs across application logs, queued review items, and exported audit artifacts

Recommended span attributes:

- `agent.id`
- `agent.version`
- `policy.version`
- `handover.id`
- `handover.trigger`
- `human.review.status`
- `human.reviewer.id`
- `human.review.duration_ms`
- `risk.level`
- `action.category`

## Framework-native overlays

Optional sources:
- LangSmith observability: https://docs.langchain.com/langsmith/observability
- LangGraph observability: https://docs.langchain.com/oss/python/langgraph/observability
- LangSmith with OpenTelemetry: https://docs.langchain.com/langsmith/trace-with-opentelemetry

Use OpenTelemetry as the portable baseline. If the stack already supports LangSmith or another agent tracing product, layer it on top rather than replacing trace IDs and structured logging.

## Audit logging rules

Design the audit trail to answer:

- What did the agent plan to do
- What triggered the handover
- What did the human see
- What did the human decide
- How long did they review it
- What happened after the decision

Prefer append-only storage, WORM storage, or tamper-evident hashing when the environment supports it.

## Recommended evidence bundle

For enterprise review or incident analysis, preserve:

- request and run identifiers
- policy snapshot or policy version
- reviewed handover packet
- human decision payload
- review duration metrics
- final execution outcome
- redaction notes when content was intentionally hidden or masked

## Redaction and privacy

Before exporting traces:

- Remove secrets, tokens, and credentials
- Mask irrelevant personal data
- Separate internal engineering telemetry from the operator-facing handover packet
- Keep the exact packet shown to the human, but redact fields that should not leave the trusted environment
