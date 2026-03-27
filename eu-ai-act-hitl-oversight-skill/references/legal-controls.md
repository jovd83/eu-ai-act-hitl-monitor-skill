# Legal Controls

Use this file when the task needs legal grounding for oversight, explainability, logging, or intervention design.

## Core articles

Primary source:
- EU AI Act Regulation (EU) 2024/1689, Official Journal, 12 July 2024: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689

Key provisions to reflect in the technical design:

- Article 12 requires logging capabilities for high-risk AI systems so events are automatically recorded during operation and the logs are sufficient to monitor functioning, support post-market monitoring, and support compliance evidence.
- Article 13 links explainability to deployer use by requiring enough transparency and instructions for use that deployers can interpret output and use the system appropriately.
- Article 14 requires effective human oversight during use, proportionate to risk, autonomy, and context.
- Article 14(4) explicitly calls for design enabling humans to:
  - understand capacities and limitations
  - detect anomalies, dysfunctions, and unexpected performance
  - remain aware of automation bias
  - correctly interpret outputs
  - decide not to use, disregard, override, or reverse output
  - intervene or interrupt the system through a stop button or similar safe halt mechanism

## Practical design implications

Translate the legal controls into product and engineering requirements:

- Do not build approval-only review flows. Provide reject, override, reverse, and halt actions.
- Do not show only raw probabilities or raw tool JSON. Provide human-readable summaries of intent, evidence, and risk.
- Do not discard intermediate trace context once the decision is made. Preserve enough audit evidence to reconstruct what happened.
- Do not hide limitations. Surface confidence, uncertainty, known failure modes, and anomaly flags.
- Do not optimize for fastest approval clicks. Measure review duration and retain operator rationale to reduce automation-bias risk.

In a pre-execution pause flow, `reverse` may be implemented as a compensating or follow-up action rather than as a primary decision enum, but the design should still preserve a clear path for undo or remediation when a side effect has already occurred.

## Minimum design checklist

Use this checklist when reviewing an agent workflow:

- Is there a defined interception policy for high-risk actions?
- Can a human understand the pending action without reading raw system traces?
- Can a human reject, override, reverse, or halt the action?
- Are review decisions recorded with timestamps and operator identity?
- Can the event be reconstructed later from logs and traces?
- Are automation-bias risks actively mitigated rather than ignored?

## Compliance posture

This skill can help design controls aligned with Articles 12 and 14, but it does not itself determine whether a concrete system is legally in scope as a high-risk AI system. If classification matters, ask for legal and product context before making scope claims.
