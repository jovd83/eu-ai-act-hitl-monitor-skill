import { z } from "zod";

export const triggerTypeSchema = z.enum([
  "low_confidence",
  "sensitive_action",
  "anomaly",
  "loop",
  "policy_violation",
]);

export const riskLevelSchema = z.enum(["low", "medium", "high", "critical"]);

export const humanOptionSchema = z.enum([
  "approve",
  "modify",
  "reject",
  "kill",
  "request_more_context",
]);

export const reviewStatusSchema = z.enum([
  "pending",
  "approve",
  "modify",
  "reject",
  "kill",
  "request_more_context",
  "timeout",
]);

export const policyDecisionSchema = z.enum([
  "allow",
  "pause_for_human_review",
  "deny",
]);

export const policyTimeoutFallbackSchema = z.enum([
  "keep_paused",
  "deny",
  "escalate",
  "safe_halt",
]);

export const reviewTimeoutFallbackSchema = z.enum([
  "keep_paused",
  "reject",
  "kill",
  "escalate",
]);

export const decisionSourceSchema = z.enum(["ui", "api", "webhook", "batch"]);

const fullHumanOptionSetSchema = z
  .array(humanOptionSchema)
  .min(5)
  .superRefine((value, ctx) => {
    const required = [
      "approve",
      "modify",
      "reject",
      "kill",
      "request_more_context",
    ] as const;
    const set = new Set(value);
    if (set.size !== value.length) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "human_options must be unique",
      });
    }
    for (const option of required) {
      if (!set.has(option)) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: `human_options missing required value: ${option}`,
        });
      }
    }
  });

const reviewStateSchema = z
  .object({
    status: reviewStatusSchema,
    reviewer_id: z.string().nullable(),
    review_started_at: z.string().datetime().nullable(),
    review_submitted_at: z.string().datetime().nullable(),
    review_duration_ms: z.number().int().min(0).nullable(),
    decision_reason: z.string().nullable(),
    modifications: z.record(z.string(), z.unknown()).nullable(),
  })
  .superRefine((value, ctx) => {
    if (
      value.review_started_at &&
      value.review_submitted_at &&
      new Date(value.review_submitted_at) < new Date(value.review_started_at)
    ) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "review_submitted_at must not be earlier than review_started_at",
        path: ["review_submitted_at"],
      });
    }

    if (value.status === "pending") {
      const fields = [
        "reviewer_id",
        "review_started_at",
        "review_submitted_at",
        "review_duration_ms",
        "decision_reason",
        "modifications",
      ] as const;
      for (const field of fields) {
        if (value[field] !== null) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: `${field} must be null when review.status is pending`,
            path: [field],
          });
        }
      }
      return;
    }

    if (value.status === "modify") {
      for (const field of [
        "reviewer_id",
        "review_started_at",
        "review_submitted_at",
        "review_duration_ms",
        "decision_reason",
      ] as const) {
        if (value[field] == null) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: `${field} is required when review.status is modify`,
            path: [field],
          });
        }
      }
      if (value.modifications == null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "modifications are required when review.status is modify",
          path: ["modifications"],
        });
      }
      return;
    }

    if (
      value.status === "approve" ||
      value.status === "reject" ||
      value.status === "kill" ||
      value.status === "request_more_context"
    ) {
      for (const field of [
        "reviewer_id",
        "review_started_at",
        "review_submitted_at",
        "review_duration_ms",
        "decision_reason",
      ] as const) {
        if (value[field] == null) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: `${field} is required when review.status is ${value.status}`,
            path: [field],
          });
        }
      }
      if (value.modifications != null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "modifications must be null unless review.status is modify",
          path: ["modifications"],
        });
      }
      return;
    }

    if (value.status === "timeout") {
      for (const field of [
        "review_submitted_at",
        "review_duration_ms",
        "decision_reason",
      ] as const) {
        if (value[field] == null) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: `${field} is required when review.status is timeout`,
            path: [field],
          });
        }
      }
      if (value.modifications != null) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "modifications must be null when review.status is timeout",
          path: ["modifications"],
        });
      }
    }
  });

export const handoverPacketSchema = z
  .object({
    example_version: z.string().min(1).optional(),
    handover_id: z.string().min(1),
    created_at: z.string().datetime(),
    trace_id: z.string().min(1),
    run_id: z.string().min(1),
    agent: z.object({
      name: z.string().min(1),
      version: z.string().min(1),
      policy_version: z.string().min(1),
    }),
    policy: z.object({
      policy_id: z.string().min(1),
      policy_version: z.string().min(1),
      policy_reference: z.string().min(1),
      review_required: z.boolean(),
    }),
    trigger: z.object({
      type: triggerTypeSchema,
      matched_rules: z.array(z.string().min(1)).min(1),
      confidence: z.number().min(0).max(1).optional(),
      risk_level: riskLevelSchema,
    }),
    pending_action: z.object({
      summary: z.string().min(1),
      tool_name: z.string().min(1),
      tool_args_redacted: z.record(z.string(), z.unknown()),
      side_effects: z.array(z.string().min(1)).min(1),
      affected_resources: z.array(z.string().min(1)).min(1),
    }),
    explanation: z.object({
      goal: z.string().min(1),
      why_now: z.string().min(1),
      evidence_summary: z.array(z.string().min(1)).min(1),
      reasoning_summary: z.string().min(1),
      uncertainty_summary: z.string().min(1),
      known_risks: z.array(z.string().min(1)).min(1),
    }),
    review_guidance: z.object({
      questions: z.array(z.string().min(1)).min(1),
      recommended_actions: z.array(z.string().min(1)).min(2),
    }),
    review_requirements: z.object({
      required_reviewer_role: z.string().min(1),
      decision_deadline_at: z.string().datetime(),
      fallback_on_timeout: reviewTimeoutFallbackSchema,
      escalation_contact: z.string().min(1).optional(),
      allow_reassignment: z.boolean(),
    }),
    human_options: fullHumanOptionSetSchema,
    audit: z.object({
      review_payload_version: z.string().min(1),
      redaction_notes: z.array(z.string().min(1)).min(1),
      evidence_refs: z.array(z.string().min(1)).min(1),
    }),
    review: reviewStateSchema,
  })
  .superRefine((value, ctx) => {
    if (new Date(value.review_requirements.decision_deadline_at) < new Date(value.created_at)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "decision_deadline_at must not be earlier than created_at",
        path: ["review_requirements", "decision_deadline_at"],
      });
    }
  });

export const modificationSchema = z.object({
  updated_action: z.string().min(1),
  changed_fields: z.array(z.string().min(1)).min(1),
  replacement_args: z.record(z.string(), z.unknown()),
  original_action_blocked: z.boolean(),
});

export const reviewDecisionSchema = z
  .object({
    example_version: z.string().min(1).optional(),
    decision_id: z.string().min(1),
    handover_id: z.string().min(1),
    reviewed_handover_version: z.string().min(1),
    decision: humanOptionSchema,
    reviewer_id: z.string().min(1),
    reviewer_role: z.string().min(1),
    decision_source: decisionSourceSchema,
    review_started_at: z.string().datetime(),
    review_submitted_at: z.string().datetime(),
    review_duration_ms: z.number().int().min(0),
    decision_reason: z.string().min(1),
    modifications: modificationSchema.nullable().optional(),
  })
  .superRefine((value, ctx) => {
    if (new Date(value.review_submitted_at) < new Date(value.review_started_at)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "review_submitted_at must not be earlier than review_started_at",
        path: ["review_submitted_at"],
      });
    }
    if (value.decision === "modify" && value.modifications == null) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "modify decisions require modifications",
        path: ["modifications"],
      });
    }
    if (value.decision !== "modify" && value.modifications != null) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "modifications must be null unless decision is modify",
        path: ["modifications"],
      });
    }
  });

export const interceptionPolicySchema = z.object({
  example_version: z.string().min(1).optional(),
  policy_id: z.string().min(1),
  policy_version: z.string().min(1),
  description: z.string().min(1),
  ownership: z
    .object({
      owner: z.string().min(1),
      escalation_contact: z.string().min(1).optional(),
    })
    .optional(),
  default_action: policyDecisionSchema,
  global_thresholds: z
    .object({
      auto_apply_min_confidence: z.number().min(0).max(1).optional(),
      high_risk_min_confidence: z.number().min(0).max(1).optional(),
      max_consecutive_failed_attempts: z.number().int().min(0).optional(),
    })
    .optional(),
  review_defaults: z
    .object({
      required_reviewer_role: z.string().min(1),
      max_review_wait_minutes: z.number().int().min(1),
      fallback_on_timeout: policyTimeoutFallbackSchema,
    })
    .optional(),
  rules: z
    .array(
      z
        .object({
          rule_id: z.string().min(1),
          trigger_type: triggerTypeSchema,
          conditions: z.record(z.string(), z.unknown()).refine(
            (value) => Object.keys(value).length > 0,
            "conditions must not be empty",
          ),
          decision: policyDecisionSchema,
          risk_level: riskLevelSchema,
          rationale: z.string().min(1),
          required_evidence: z.array(z.string().min(1)).min(1),
          human_options: fullHumanOptionSetSchema.optional(),
          required_reviewer_role: z.string().min(1).optional(),
          max_review_wait_minutes: z.number().int().min(1).optional(),
          fallback_on_timeout: policyTimeoutFallbackSchema.optional(),
        })
        .superRefine((value, ctx) => {
          if (
            value.decision === "pause_for_human_review" &&
            value.human_options == null
          ) {
            ctx.addIssue({
              code: z.ZodIssueCode.custom,
              message:
                "pause_for_human_review rules require the full human option set",
              path: ["human_options"],
            });
          }
          if (
            value.decision !== "pause_for_human_review" &&
            (value.human_options != null ||
              value.required_reviewer_role != null ||
              value.max_review_wait_minutes != null ||
              value.fallback_on_timeout != null)
          ) {
            ctx.addIssue({
              code: z.ZodIssueCode.custom,
              message:
                "human review fields are only allowed when decision is pause_for_human_review",
              path: ["decision"],
            });
          }
        }),
    )
    .min(1),
});

export type HandoverPacket = z.infer<typeof handoverPacketSchema>;
export type ReviewDecision = z.infer<typeof reviewDecisionSchema>;
export type InterceptionPolicy = z.infer<typeof interceptionPolicySchema>;
