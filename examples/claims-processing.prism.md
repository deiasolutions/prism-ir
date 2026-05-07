---
prism: claims-processing
version: 1.3.0
---

# Claims Processing

This is the example workflow rendered in the LinkedIn announcement image
for PRISM-IR ("The lingua franca between code and business").

The natural-language description below describes the same process as the
YAML IR that follows. Both describe the same six-step workflow. They are
intended to round-trip through an LLM: an LLM should be able to
reconstruct this English description from the IR alone, and produce
equivalent IR from this description alone. If the round-trip fails, the
IR is wrong.

## Natural Language

1. Customer submits claim
2. System validates policy status
3. If policy inactive, reject claim
4. If claim amount exceeds threshold, route to manual review
5. Otherwise approve automatically
6. Notify customer and archive decision

## PRISM-IR

```yaml
v: "1.0"
id: "claims-processing"
name: "Claims Processing"
domain: "insurance"

intention: "Decide insurance claims"
failure_tolerance: "any"

constraints:
  sla: "95% within 24 hours"
  fail: ">72h"
  priority: "accuracy > speed"

vocabulary:
  - term: "claim"
    maps_to: "entity.type == 'insurance_claim'"
  - term: "high-value"
    maps_to: "entity.amount > params.review_threshold"
  - term: "active-policy"
    maps_to: "entity.policy_status == 'active'"

entities:
  - type: insurance_claim
    attrs:
      - { name: claim_id,       dtype: string, required: true }
      - { name: policy_id,      dtype: string, required: true }
      - { name: customer_id,    dtype: string, required: true }
      - { name: amount,         dtype: number, required: true }
      - { name: policy_status,  dtype: enum, values: [active, inactive, lapsed], default: active }
      - { name: decision,       dtype: enum, values: [approved, rejected, pending], default: pending }
      - { name: decision_reason, dtype: string }
    lifecycle: [submitted, validating, deciding, notifying, archived]

events:
  - id: evt_claim_decided
    type: persistent
    payload:
      - { name: claim_id, dtype: string }
      - { name: decision, dtype: string }
      - { name: amount,   dtype: number }

generators:
  - id: claim_arrivals
    entity: insurance_claim
    arrival:
      distribution: poisson
      rate: 50

resources:
  - id: underwriters
    capacity: 10
    skills: [manual_review]
    schedule:
      shifts:
        - name: day
          hours: "09:00-17:00"
          capacity: 10

nodes:
  - id: e1a7f9c2
    name: StartEvent
    t: start

  - id: t1d2a3b4
    name: ValidatePolicy
    t: task
    o: { op: api }
    intention: "Confirm the policy backing this claim is active"

  - id: df3e5c7
    name: PolicyActive?
    t: decision
    mode: exclusive
    out:
      active:   d4b6a8f0
      inactive: t2e6b8a1

  - id: t2e6b8a1
    name: RejectClaim
    t: task
    o: { op: api }
    intention: "Reject claim due to inactive policy"
    a:
      - type: set
        path: "entity.decision"
        value: "rejected"
      - type: set
        path: "entity.decision_reason"
        value: "InactivePolicy"

  - id: d4b6a8f0
    name: AmountThreshold?
    t: decision
    mode: exclusive
    out:
      over_threshold:  t3c7d9e2
      under_threshold: t4f8a0b3

  - id: t3c7d9e2
    name: ManualReview
    t: task
    o: { op: human, tier: 4 }
    intention: "Underwriter reviews high-value claim"

  - id: t4f8a0b3
    name: AutoApprove
    t: task
    o: { op: script }
    intention: "Apply default approval rule"
    a:
      - type: set
        path: "entity.decision"
        value: "approved"

  - id: t5a1b2c2
    name: NotifyCustomer
    t: task
    o: { op: api }
    intention: "Send claim decision to customer"

  - id: t6d4e5f6
    name: ArchiveDecision
    t: task
    o: { op: api }
    intention: "Write decision to audit log"
    a:
      - type: emit
        event: evt_claim_decided
        payload:
          claim_id: "${entity.claim_id}"
          decision: "${entity.decision}"
          amount:   "${entity.amount}"

  - id: e9f8d7c6
    name: EndEvent
    t: end

edges:
  - { s: e1a7f9c2, t: t1d2a3b4 }
  - { s: t1d2a3b4, t: df3e5c7 }
  - { s: df3e5c7,  t: t2e6b8a1, c: "entity.policy_status != 'active'" }
  - { s: df3e5c7,  t: d4b6a8f0, c: "entity.policy_status == 'active'" }
  - { s: d4b6a8f0, t: t3c7d9e2, c: "entity.amount > params.review_threshold" }
  - { s: d4b6a8f0, t: t4f8a0b3, c: "entity.amount <= params.review_threshold" }
  - { s: t2e6b8a1, t: t5a1b2c2 }
  - { s: t3c7d9e2, t: t5a1b2c2 }
  - { s: t4f8a0b3, t: t5a1b2c2 }
  - { s: t5a1b2c2, t: t6d4e5f6 }
  - { s: t6d4e5f6, t: e9f8d7c6 }

metrics:
  - cycle_time
  - sla_compliance
  - approval_rate
  - manual_review_rate

params:
  review_threshold: 10000
```

## Provenance

This file matches the workflow shown in the LinkedIn announcement image
for PRISM-IR. Identifiers in the `nodes` block correspond to the node
IDs visible in the rendered graph.

| Field        | Value                          |
|--------------|--------------------------------|
| artifact     | prism://process/claims/v1      |
| version      | 1.3.0                          |
| schema       | prism://schema/v1.0.0          |
| dsl          | prism-ir@1.0                   |
| owner        | claims-team                    |
| status       | active                         |
