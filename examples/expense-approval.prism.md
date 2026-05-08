---
prism: expense-approval
version: 1.0.0
---

# Expense Approval

A simple human-reviewed approval flow. The README's quick example,
formalized as a runnable PRISM-IR file with both the natural-language
description and the IR.

## Natural Language

We need to approve employee expenses. A reviewer looks at each claim and
either approves or rejects it. Ninety-five percent of decisions should
be made within twenty-four hours.

## PRISM-IR

```yaml
v: "1.0"
id: "expense_approval"
name: "Expense Approval"
domain: "finance"

intention: "Approve employee expenses"
failure_tolerance: "any"

constraints:
  sla: "95% within 24 hours"
  fail: ">48h"

entities:
  - type: expense_claim
    attrs:
      - { name: employee_id, dtype: string, required: true }
      - { name: amount,      dtype: number, required: true }
      - { name: category,    dtype: string }
      - { name: outcome,     dtype: enum, values: [approved, rejected, pending], default: pending }
    lifecycle: [submitted, reviewing, decided]

events:
  - id: evt_approved
    type: transient
    payload:
      - { name: claim_id, dtype: string }

nodes:
  - id: start
    t: start

  - id: review
    t: task
    o: { op: human }
    intention: "Reviewer evaluates the expense claim"
    failure_policy:
      retry: 1
      if_all_fail: escalate

  - id: decision
    t: decision
    mode: exclusive
    out:
      approved: end_approved
      rejected: end_rejected

  - id: end_approved
    t: end
    a:
      - type: emit
        event: evt_approved
        payload:
          claim_id: "${entity.id}"

  - id: end_rejected
    t: end

edges:
  - { s: start,    t: review }
  - { s: review,   t: decision }
  - { s: decision, t: end_approved, c: "outcome == 'approved'" }
  - { s: decision, t: end_rejected, c: "outcome == 'rejected'" }

metrics:
  - cycle_time
  - sla_compliance
```
