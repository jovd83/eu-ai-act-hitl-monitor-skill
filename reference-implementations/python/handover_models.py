#!/usr/bin/env python3
"""Reference Pydantic models for policy, handover, and review contracts."""

from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


ROOT = Path(__file__).resolve().parents[2]


class TriggerType(str, Enum):
    LOW_CONFIDENCE = "low_confidence"
    SENSITIVE_ACTION = "sensitive_action"
    ANOMALY = "anomaly"
    LOOP = "loop"
    POLICY_VIOLATION = "policy_violation"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class HumanOption(str, Enum):
    APPROVE = "approve"
    MODIFY = "modify"
    REJECT = "reject"
    KILL = "kill"
    REQUEST_MORE_CONTEXT = "request_more_context"


class ReviewStatus(str, Enum):
    PENDING = "pending"
    APPROVE = "approve"
    MODIFY = "modify"
    REJECT = "reject"
    KILL = "kill"
    REQUEST_MORE_CONTEXT = "request_more_context"
    TIMEOUT = "timeout"


class PolicyDecision(str, Enum):
    ALLOW = "allow"
    PAUSE_FOR_HUMAN_REVIEW = "pause_for_human_review"
    DENY = "deny"


class PolicyTimeoutFallback(str, Enum):
    KEEP_PAUSED = "keep_paused"
    DENY = "deny"
    ESCALATE = "escalate"
    SAFE_HALT = "safe_halt"


class ReviewTimeoutFallback(str, Enum):
    KEEP_PAUSED = "keep_paused"
    REJECT = "reject"
    KILL = "kill"
    ESCALATE = "escalate"


class DecisionSource(str, Enum):
    UI = "ui"
    API = "api"
    WEBHOOK = "webhook"
    BATCH = "batch"


def require_full_human_option_set(options: list[HumanOption]) -> list[HumanOption]:
    required = {
        HumanOption.APPROVE,
        HumanOption.MODIFY,
        HumanOption.REJECT,
        HumanOption.KILL,
        HumanOption.REQUEST_MORE_CONTEXT,
    }
    if len(set(options)) != len(options):
        raise ValueError("human options must be unique")
    missing = required - set(options)
    if missing:
        raise ValueError(f"human options missing required values: {sorted(item.value for item in missing)}")
    return options


def ensure_time_order(start: datetime | None, end: datetime | None, *, label: str) -> None:
    if start is not None and end is not None and end < start:
        raise ValueError(f"{label} end timestamp must not be earlier than start timestamp")


class AgentInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    version: str
    policy_version: str


class PolicyRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_id: str
    policy_version: str
    policy_reference: str
    review_required: bool


class Trigger(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: TriggerType
    matched_rules: list[str] = Field(min_length=1)
    confidence: float | None = Field(default=None, ge=0, le=1)
    risk_level: RiskLevel


class PendingAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str
    tool_name: str
    tool_args_redacted: dict[str, Any]
    side_effects: list[str] = Field(min_length=1)
    affected_resources: list[str] = Field(min_length=1)


class Explanation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    goal: str
    why_now: str
    evidence_summary: list[str] = Field(min_length=1)
    reasoning_summary: str
    uncertainty_summary: str
    known_risks: list[str] = Field(min_length=1)


class ReviewGuidance(BaseModel):
    model_config = ConfigDict(extra="forbid")

    questions: list[str] = Field(min_length=1)
    recommended_actions: list[str] = Field(min_length=2)


class ReviewRequirements(BaseModel):
    model_config = ConfigDict(extra="forbid")

    required_reviewer_role: str
    decision_deadline_at: datetime
    fallback_on_timeout: ReviewTimeoutFallback
    escalation_contact: str | None = None
    allow_reassignment: bool


class AuditEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    review_payload_version: str
    redaction_notes: list[str] = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)


class Review(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: ReviewStatus
    reviewer_id: str | None = None
    review_started_at: datetime | None = None
    review_submitted_at: datetime | None = None
    review_duration_ms: int | None = Field(default=None, ge=0)
    decision_reason: str | None = None
    modifications: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_review_state(self) -> "Review":
        ensure_time_order(self.review_started_at, self.review_submitted_at, label="review")

        if self.status == ReviewStatus.PENDING:
            if any(
                value is not None
                for value in (
                    self.reviewer_id,
                    self.review_started_at,
                    self.review_submitted_at,
                    self.review_duration_ms,
                    self.decision_reason,
                    self.modifications,
                )
            ):
                raise ValueError("pending review state must not contain reviewer outcome fields")
            return self

        if self.status == ReviewStatus.TIMEOUT:
            if self.review_submitted_at is None or self.review_duration_ms is None or self.decision_reason is None:
                raise ValueError("timeout review state requires review_submitted_at, review_duration_ms, and decision_reason")
            if self.modifications is not None:
                raise ValueError("timeout review state must not contain modifications")
            return self

        required_values = {
            "reviewer_id": self.reviewer_id,
            "review_started_at": self.review_started_at,
            "review_submitted_at": self.review_submitted_at,
            "review_duration_ms": self.review_duration_ms,
            "decision_reason": self.decision_reason,
        }
        for field_name, value in required_values.items():
            if value is None:
                raise ValueError(f"{field_name} is required when review status is {self.status.value}")

        if self.status == ReviewStatus.MODIFY:
            if self.modifications is None:
                raise ValueError("modify review state requires modifications")
        elif self.modifications is not None:
            raise ValueError("modifications must be null unless review status is modify")

        return self


class HandoverPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    example_version: str | None = None
    handover_id: str
    created_at: datetime
    trace_id: str
    run_id: str
    agent: AgentInfo
    policy: PolicyRef
    trigger: Trigger
    pending_action: PendingAction
    explanation: Explanation
    review_guidance: ReviewGuidance
    review_requirements: ReviewRequirements
    human_options: list[HumanOption] = Field(min_length=5)
    audit: AuditEnvelope
    review: Review

    @model_validator(mode="after")
    def validate_human_options(self) -> "HandoverPacket":
        self.human_options = require_full_human_option_set(self.human_options)
        if self.review_requirements.decision_deadline_at < self.created_at:
            raise ValueError("review decision deadline must not be earlier than handover creation time")
        return self


class Modification(BaseModel):
    model_config = ConfigDict(extra="forbid")

    updated_action: str
    changed_fields: list[str] = Field(min_length=1)
    replacement_args: dict[str, Any]
    original_action_blocked: bool


class ReviewDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    example_version: str | None = None
    decision_id: str
    handover_id: str
    reviewed_handover_version: str
    decision: HumanOption
    reviewer_id: str
    reviewer_role: str
    decision_source: DecisionSource
    review_started_at: datetime
    review_submitted_at: datetime
    review_duration_ms: int = Field(ge=0)
    decision_reason: str
    modifications: Modification | None = None

    @model_validator(mode="after")
    def validate_modification_rules(self) -> "ReviewDecision":
        ensure_time_order(self.review_started_at, self.review_submitted_at, label="decision review")
        if self.decision == HumanOption.MODIFY and self.modifications is None:
            raise ValueError("modify decisions require modifications")
        if self.decision != HumanOption.MODIFY and self.modifications is not None:
            raise ValueError("modifications must be null unless decision is modify")
        return self


class PolicyOwnership(BaseModel):
    model_config = ConfigDict(extra="forbid")

    owner: str
    escalation_contact: str | None = None


class PolicyThresholds(BaseModel):
    model_config = ConfigDict(extra="forbid")

    auto_apply_min_confidence: float | None = Field(default=None, ge=0, le=1)
    high_risk_min_confidence: float | None = Field(default=None, ge=0, le=1)
    max_consecutive_failed_attempts: int | None = Field(default=None, ge=0)


class ReviewDefaults(BaseModel):
    model_config = ConfigDict(extra="forbid")

    required_reviewer_role: str
    max_review_wait_minutes: int = Field(ge=1)
    fallback_on_timeout: PolicyTimeoutFallback


class PolicyRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str
    trigger_type: TriggerType
    conditions: dict[str, Any]
    decision: PolicyDecision
    risk_level: RiskLevel
    rationale: str
    required_evidence: list[str] = Field(min_length=1)
    human_options: list[HumanOption] | None = None
    required_reviewer_role: str | None = None
    max_review_wait_minutes: int | None = Field(default=None, ge=1)
    fallback_on_timeout: PolicyTimeoutFallback | None = None

    @model_validator(mode="after")
    def validate_human_options_for_pause(self) -> "PolicyRule":
        if not self.conditions:
            raise ValueError("conditions must not be empty")
        if self.decision == PolicyDecision.PAUSE_FOR_HUMAN_REVIEW:
            if self.human_options is None:
                raise ValueError("pause_for_human_review rules require human_options")
            self.human_options = require_full_human_option_set(self.human_options)
        elif any(
            value is not None
            for value in (
                self.human_options,
                self.required_reviewer_role,
                self.max_review_wait_minutes,
                self.fallback_on_timeout,
            )
        ):
            raise ValueError(
                "human review fields are only allowed when decision is pause_for_human_review"
            )
        return self


class InterceptionPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    example_version: str | None = None
    policy_id: str
    policy_version: str
    description: str
    ownership: PolicyOwnership | None = None
    default_action: PolicyDecision
    global_thresholds: PolicyThresholds | None = None
    review_defaults: ReviewDefaults | None = None
    rules: list[PolicyRule] = Field(min_length=1)


def load_fixture(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    InterceptionPolicy.model_validate(load_fixture(ROOT / "examples" / "interception-policy.example.json"))
    HandoverPacket.model_validate(load_fixture(ROOT / "examples" / "handover-packet.example.json"))
    HandoverPacket.model_validate(load_fixture(ROOT / "examples" / "bug-fix-handover-packet.example.json"))
    HandoverPacket.model_validate(load_fixture(ROOT / "examples" / "feature-implementation-handover-packet.example.json"))
    ReviewDecision.model_validate(load_fixture(ROOT / "examples" / "review-decision.example.json"))
    ReviewDecision.model_validate(load_fixture(ROOT / "examples" / "bug-fix-review-decision.example.json"))
    ReviewDecision.model_validate(load_fixture(ROOT / "examples" / "feature-implementation-review-decision.example.json"))
    print("Pydantic reference models validated all bundled examples successfully.")
