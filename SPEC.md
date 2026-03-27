# PRISM-IR Specification v1.0

**PRISM** = Process Representation, Intent Simulation & Manifestation
**PRISM-IR** = the Intermediate Representation of the PRISM spec

**Version:** 1.0.0
**Status:** Public
**Published by:** DEIA Solutions / deiasolutions.com
**Repository:** github.com/deiasolutions/prism-ir

---

## What Is PRISM-IR?

PRISM-IR is a domain-agnostic intermediate representation for describing
any process -- simulated, executed, or hybrid. It is the contract
between human intent and machine execution, written and read by LLMs.

Humans describe processes in plain English. LLMs translate that English
into PRISM-IR. Runtimes execute the IR. LLMs can reconstruct the English
from the IR at any time. Humans never need to read or write YAML.

An **Intermediate Representation (IR)** is a normalized internal form
that sits between input (English, BPMN, L-systems, etc.) and execution.
It is the translation layer that lets one spec run four different ways.

> "If a thing can be described in words, we can simulate it with an LLM,
> and operationalize it with Operators."

PRISM-IR is not a programming language. It is not a workflow engine. It
is a specification format authored by LLMs, executed by conforming
runtimes, and readable by any LLM at any time.

---

## Who Writes PRISM-IR?

LLMs write PRISM-IR. Humans write English.

| Who | What They Do |
|-----|-------------|
| **Human** | Describes the process in plain English |
| **LLM** | Translates English into PRISM-IR |
| **Runtime** | Executes the IR |
| **LLM** | Reconstructs English from IR on demand |

The expression language, join policy tables, operator schemas, and
resource dispatch modes in this spec are a precise vocabulary for LLMs
to reason about process structure without ambiguity. They are not a
learning curve for human developers. Humans work at the intention layer.
LLMs work at the IR layer.

---

## Core Thesis

One PRISM-IR file. Four execution modes. Same spec, same intent, same
measurement.

| Mode | What Happens |
|------|-------------|
| **Simulation** | Run in virtual time. Explore branches. Find failure modes before they happen. |
| **Production** | Execute against real operators: humans, APIs, LLMs, scripts. |
| **Hybrid** | Mix simulation and production in the same flow. Some nodes real, some virtual. |
| **Optimization** | ML learns from simulation and production runs. Returns Pareto-optimal configurations. |

The flow definition never changes between modes. Only operator bindings change.

---

## Key Concepts

### Intention

Every process -- and every sub-process within it -- has an intention.
Intention is the goal. A verb and an object. Why this process exists.

Intention is first-class in PRISM-IR. Without "why," a process is a
black box. With it, the platform can measure whether execution matched
intent.

### Intermediate Representation

The IR is a graph of nodes connected by edges, carrying tokens through
a defined flow. It sits between input languages (English, BPMN, SBML,
L-systems) and execution engines (DES, production runtime, optimizer).
Input languages compile into PRISM-IR. PRISM-IR executes. Results emit
to the Event Ledger.

### The Round-Trip Guarantee

English -> IR -> English. If the round-trip loses meaning, the IR is
wrong. This guarantee exists not for human readability but for
LLM-to-LLM fidelity. Any LLM receiving a PRISM-IR file must be able to
reconstruct the original intent accurately, without hallucination or
drift. The round-trip is a correctness test for the IR, not a
documentation feature.

### The Alterverse

Every branch taken creates a timeline. The Alterverse is the tree of all
timelines: every simulation branch, every production run, every
counterfactual. Nothing is deleted. Every path is queryable.

---

## File Format

A PRISM-IR file uses the `.prism.md` extension with YAML frontmatter:

```yaml
---
prism: my-flow
version: 1.0.0
---
```

The body is a YAML fenced block containing the flow definition.
Conforming runtimes may also support PRISM-IR as an embedded block type
within their own package formats.

---

## Top-Level Schema

```yaml
v: "1.0"                          # PRISM-IR version. Required.
id: string                         # Unique flow identifier. Required.
name: string                       # Human-readable name. Required.
domain: string                     # Domain context for vocabulary. Optional.

# What this process is for
intention: string                  # The goal. Verb + object. Required.

# How much failure to absorb before halting
failure_tolerance: expression      # See Failure Tolerance section.

# Performance and quality rules
constraints:
  sla: string                      # SLA target
  fail: string                     # What constitutes a miss
  priority: string                 # Trade-off guidance

# Domain-specific vocabulary bindings
vocabulary:
  - term: string
    maps_to: expression

# Entity type definitions
entities: [...]

# Event type declarations (all emitted events must be declared here)
events: [...]

# Token arrival generators
generators: [...]

# Queue definitions
queues: [...]

# Resource pools
resources: [...]

# Sub-process groupings
groups: [...]

# Surrogate model bindings
surrogates: [...]

# Graph nodes
nodes: [...]

# Graph edges
edges: [...]

# Phase boundaries (metamorphosis points)
phase_boundaries: [...]

# Metrics to collect
metrics: [...]

# Flow-level parameters (tunable at runtime)
params: {}
```

---

## Intention and Constraints

### Intention

Intention is singular and simple. It answers: why does this process
exist?

```yaml
intention: "Approve loans"
```

### Constraints

Constraints govern how well the process must perform. They are sub-keys
of the `constraints` block:

```yaml
constraints:
  sla: "95% within 4 hours"     # Measurable target
  fail: ">24h"                   # What constitutes a miss
  priority: "speed > thoroughness"  # Trade-off guidance
```

### Failure Tolerance

Failure tolerance is a peer of `constraints`, not nested within it. It
governs resilience: how much failure to absorb before halting. It answers
a different question than constraints (which govern success, not
survival).

```yaml
failure_tolerance: "5%"
```

Failure tolerance grammar:

| Expression | Meaning |
|------------|---------|
| `"5%"` | Halt if more than 5% of work items fail |
| `"2 consecutive"` | Halt after 2 failures in a row |
| `"3 in 1h"` | Halt after 3 failures within any 1-hour window |
| `"any"` | Zero tolerance -- first failure halts |
| `"unlimited"` | Never halt on failure (log only) |

### Inheritance

Intention and constraints cascade like CSS. Flow sets defaults. Groups
can narrow or specialize. Nodes can override for their scope. Most
specific wins.

```yaml
flow:
  intention: "Approve loans"
  constraints:
    sla: "95% within 4 hours"

groups:
  - id: identity_verification
    intention: "Verify identity"
    constraints:
      sla: "100% within 10 minutes"   # Tighter than flow

nodes:
  - id: credit_check
    constraints:
      timeout: "30 seconds"           # Node-specific, inherits rest
```

---

## Node Types

Every node has a type field `t:` indicating its role in the graph.

| Type | Shorthand `t:` | Description |
|------|----------------|-------------|
| Start | `start` | Entry point. Every flow has exactly one. |
| End | `end` | Terminal node. A flow may have multiple. |
| Task | `task` | A unit of work executed by an operator. |
| Decision | `decision` | Routes tokens based on conditions. |
| Fork | `fork` | Splits one token into N parallel tokens. |
| Join | `join` | Merges N tokens into one. |
| Vote | `vote` | Collects verdicts from N participants, applies resolution policy. |
| Checkpoint | `checkpoint` | Evaluates a condition; may trigger a phase boundary. |
| Event Wait | `event_wait` | Holds token until a named event arrives. |
| Cancel | `cancel` | Terminates tokens within a scope. |
| Queue | `queue` | Buffers tokens under a queue discipline. |

### Decision Modes

| Mode | Behavior |
|------|----------|
| `exclusive` | Exactly one outgoing edge fires (XOR) |
| `multi` | One or more outgoing edges fire (OR) |
| `parallel` | All outgoing edges fire (AND) -- use `fork` instead when intent is always-parallel |

### Fork

```yaml
- id: parallel_review
  t: fork
  # All outgoing edges fire unconditionally
```

### Join

```yaml
- id: review_join
  t: join
  joinPolicy:
    mode: all           # Wait for all incoming tokens
```

Join policies:

| Mode | Behavior |
|------|----------|
| `all` | Wait for all incoming tokens (synchronization) |
| `any` | Fire on first arriving token |
| `first_of_m` | Fire on first, optionally block or cancel others |
| `n_of_m` | Fire when N of M tokens arrive |
| `all_taken` | Wait for exactly the branches that fired (structured sync) |
| `interleaved` | Tokens take turns; mutex prevents concurrency |

Join modifiers:

```yaml
joinPolicy:
  mode: n_of_m
  n: 2
  m: 3
  onSatisfied: cancel_pending   # Cancel remaining tokens when satisfied
  onCancel: log                 # log | discard | archive
  structured: true              # Structured sync -- tracks lineage
  local: true                   # Local synchronizing merge
  block_others: true            # Blocking discriminator
  cancel_others: true           # Canceling discriminator
  autoTerminate: true           # Flow terminates when no tokens remain
  maxDepth: 10                  # Recursion depth limit
```

### Vote

A vote node collects verdicts from N parallel participants and applies a
resolution policy. Used when parallel review requires aggregated
judgment, not just synchronization.

```yaml
- id: review_vote
  t: vote
  mode: majority          # majority | unanimous | threshold
  verdict_expr: "result.outcome == 'approved'"
  tie_breaker:
    policy: escalate      # escalate | senior_reviewer | auto_approve | auto_reject
    operator: { op: human, tier: 4 }
  out:
    approved: end_approved
    rejected: end_rejected
    tie: tie_breaker_node
```

Vote outcomes for a 3-reviewer majority vote:

| Verdicts | Result |
|----------|--------|
| YYY | approved |
| NNN | rejected |
| YYN / YNY / NYY | approved (majority) |
| YNN / NYN / NNY | rejected (majority) |
| YN (2 reviewers, tied) | tie -- escalates |

### Checkpoint

A checkpoint marks where metamorphosis may occur. It evaluates a
condition and optionally triggers a phase boundary.

```yaml
- id: scale_ready
  t: checkpoint
  phase_gate:
    evaluate: "metrics.revenue > 10000000"
    if_true:
      trigger_boundary: "pivot_to_enterprise"
    if_false:
      continue: normal
```

---

## Operators

An operator is the entity that executes a task node. PRISM-IR treats
LLMs, humans, APIs, and scripts as interchangeable at the node level.
The platform does not care who executes -- it routes, waits, collects,
and moves on.

### Operator Types

```yaml
o: { op: llm }           # LLM (any provider)
o: { op: llm, tier: 2 }  # LLM at a specific oracle tier
o: { op: human }         # Human participant
o: { op: api }           # External API call
o: { op: script }        # Deterministic script
o: { op: external }      # External system
o: { op: surrogate, model: surrogate_id }  # Trained surrogate model
o: { op: auto }          # Platform chooses based on cost/quality/time
```

### Oracle Tiers (LLM Routing)

| Tier | Description |
|------|-------------|
| 0 | Local model (no cost, limited capability) |
| 1 | Fast cheap model |
| 2 | Standard capable model |
| 3 | Advanced model |
| 4 | Human (maximum capability, maximum cost) |

### Failure Policies

```yaml
- id: credit_check
  t: task
  o:
    op: llm
    tier: 2
  failure_policy:
    retry: 2
    then: failover
    fallback: { op: llm, tier: 3 }
    failover_retry: 2
    then: escalate
    block_failed_for: "10 min"
    if_all_fail: skip       # skip | halt | escalate
```

Failure responses:

| Response | Behavior |
|----------|----------|
| `retry` | Try same operator again with backoff |
| `failover` | Switch to fallback operator |
| `block` | Mark operator unavailable for N time |
| `escalate` | Bump to higher tier |
| `skip` | Mark item failed, continue flow |
| `halt` | Stop execution (circuit breaker) |

---

## Tokens and Entities

### Token

A token is an instance of execution flowing through the graph. It
carries an entity through the process.

| Concept | What It Is |
|---------|-----------|
| Token | Active execution marker at a node |
| Entity | The work item the token carries |
| Position | Which node the token currently occupies |
| State | Entity attributes and accumulated variables |
| Lineage | Path history (required for structured sync) |

Token lifecycle:

```
Generator creates token
    |
Token enters Start node
    |
Token moves along edges
    |
At fork: one token becomes N tokens
    |
At join: N tokens become one token
    |
Token reaches End: consumed
```

Token operations: Create, Move, Fork, Merge, Cancel, Complete.

### Token Schema (Runtime)

```yaml
token:
  id: "tok_a1b2c3"
  entity:
    type: "loan_application"
    id: "loan_7890"
    attrs:
      applicant_id: "cust_123"
      amount: 50000
      risk_score: 0.3
      priority: "standard"
  position: "node_credit_check"
  status: "active"    # active | waiting | completed | cancelled
  lineage:
    - split: "node_fork_1"
      branch: "branch_b"
      at: "2026-01-01T10:30:00Z"
  variables:
    approval_count: 0
    reviewer_notes: []
  created_at: "2026-01-01T10:00:00Z"
  updated_at: "2026-01-01T10:30:00Z"
```

### Entity Schema

```yaml
entities:
  - type: loan_application
    attrs:
      - name: applicant_id
        dtype: string
        required: true
      - name: amount
        dtype: number
        required: true
      - name: risk_score
        dtype: number
        default: null
      - name: priority
        dtype: enum
        values: [standard, vip, expedited]
        default: standard
    lifecycle:
      - submitted
      - reviewing
      - decided
      - closed
```

---

## Events

All events emitted anywhere in the flow must be declared in the
top-level `events:` block. Emitting an undeclared event is a validation
error.

```yaml
events:
  - id: evt_fraud_alert
    type: persistent        # transient | persistent
    payload:
      - name: alert_level
        dtype: number
      - name: flagged_by
        dtype: string

  - id: evt_loan_approved
    type: transient
    payload:
      - name: loan_id
        dtype: string
      - name: amount
        dtype: number
```

Event types:

| Type | Behavior |
|------|----------|
| `transient` | Consumed by first waiting listener; lost if no listener |
| `persistent` | Held until consumed; survives timeouts |

### Emitting Events

```yaml
- id: end_approved
  t: end
  a:
    - type: emit
      event: evt_loan_approved
      payload:
        loan_id: "${entity.id}"
        amount: "${entity.amount}"
```

### Waiting for Events

```yaml
- id: wait_for_document
  t: event_wait
  trigger:
    event: evt_document_received
    timeout: "24h"
    onTimeout: escalate
```

### Event-Triggered Edges

```yaml
edges:
  - s: idle_state
    t: fraud_handler
    trigger:
      type: event
      event: evt_fraud_alert
```

---

## Generators

Generators create tokens (work items) and inject them into the flow.

```yaml
generators:
  - id: loan_arrivals
    entity: loan_application
    arrival:
      distribution: poisson   # poisson | exponential | normal | uniform | batch | schedule | data
      rate: 12                # per hour
    warmup: "5 min"
    schedule: "09:00-17:00 weekdays"
```

---

## Queues

```yaml
queues:
  - id: main_queue
    discipline: fifo        # fifo | lifo | priority | shortest_job
    priority_expr: "entity.priority == 'vip'"
    capacity: unlimited     # unlimited | number
    reneging:
      timeout: "5 min"
      action: abandon       # abandon | escalate | retry
      emit: evt_caller_abandoned
    balking:
      condition: "len(queue) > 20"
      action: abandon       # abandon | route_elsewhere
```

---

## Resources

Resources are pools of capacity available to task nodes. They may be
human agents, LLM instances, machines, or any constrained asset.

### Four-Vector Profile

Each resource pool carries a statistical profile per skill. The four
vectors measure:

| Vector | Symbol | What It Measures |
|--------|--------|-----------------|
| Quality | sigma | How well they perform |
| Preference | pi | What tasks they gravitate toward |
| Autonomy | alpha | How independently they operate |
| Reliability | rho | How consistently they deliver |

Each vector is per-domain -- an agent's quality for sales is independent
of their quality for customer service.

```yaml
resources:
  - id: senior_reviewers
    capacity: 5
    skills: [high_risk, escalation]
    priority: [high_risk, escalation]

    profile:
      high_risk:
        sigma: { dist: normal, mean: 0.85, std: 0.08 }
        pi:    { dist: normal, mean: 0.75, std: 0.12 }
        alpha: { dist: normal, mean: 0.60, std: 0.15 }
        rho:   { dist: normal, mean: 0.90, std: 0.06 }
        correlations:
          - [sigma, rho, 0.6]      # quality correlates with reliability
          - [alpha, sigma, -0.2]   # more autonomous slightly lower quality
          - [pi, rho, 0.3]         # prefer the work more reliable

    schedule:
      shifts:
        - name: day
          hours: "09:00-17:00"
          capacity: 5
      breaks:
        - type: lunch
          duration: 30min
          stagger: true
          window: "11:00-14:00"

    dispatch:
      mode: scored            # longest_idle | scored | matrix | decision_tree
      tiebreaker: longest_idle
      scoring:
        factors:
          - name: skill_match
            weight: 40
            expr: "agent.skills contains entity.skill_needed ? 1.0 : 0.0"
          - name: quality
            weight: 60
            expr: "agent.profile[entity.skill_needed].sigma"

    allocation:
      mode: priority          # priority | round_robin | weighted | balanced
      priority: [high_risk, escalation]
```

---

## Expression Language

PRISM-IR uses a Python-like expression syntax for guards, conditions,
variable references, and vocabulary mappings. This grammar is the
precise vocabulary LLMs use when authoring PRISM-IR. It is designed to
be unambiguous inside YAML strings and to read like English so that
LLMs can generate, validate, and reason about expressions reliably.

### Syntax

```
# Atoms
identifier     := [a-zA-Z_][a-zA-Z0-9_]*
path           := identifier ('.' identifier)*
string         := "'" [^']* "'"       # Single quotes only
number         := [0-9]+ ('.' [0-9]+)?
boolean        := 'true' | 'false'
null           := 'null'
duration       := number ('ms' | 's' | 'min' | 'h' | 'd')

# Operators
comparison     := '==' | '!=' | '<' | '<=' | '>' | '>='
logical        := 'and' | 'or' | 'not'
membership     := 'in' | 'not in'
arithmetic     := '+' | '-' | '*' | '/' | '%'
```

### Namespace

| Root | What It Is | Available In |
|------|-----------|--------------|
| `entity` | The work item carried by the token | All token contexts |
| `token` | The execution marker itself | All token contexts |
| `node` | Current or referenced node | Guards, actions, conditions |
| `source` | Node the token came from | Edge conditions |
| `target` | Node the token is going to | Edge conditions |
| `result` | Output from node execution | Actions (post-execution) |
| `tokens` | All tokens at a join | Join conditions |
| `flow` | The overall process instance | Everywhere |
| `metrics` | Aggregated measurements | Constraints, phase gates |
| `params` | Flow-level parameters | Everywhere |
| `now` | Current time (simulation or wall clock) | Everywhere |
| `agent` | Resource assigned to current task | Dispatch scoring |
| `queue` | Named queue | Queue conditions |

### Differences From Python

PRISM-IR expressions are intentionally Python-like but not Python. The
differences are deliberate, not oversight. PRISM-IR expressions are
always embedded inside YAML strings, which imposes two hard constraints:
double quotes delimit YAML strings, so they cannot be used inside them
without escaping; and bracket notation (`entity["attr"]`) produces
ambiguous parse results inside a quoted YAML value. The deviations below
resolve both problems cleanly.

| Feature | Python | PRISM-IR | Why |
|---------|--------|----------|-----|
| Variable access | `entity["attr"]` | Always dot: `entity.attr` | Brackets are ambiguous inside YAML strings |
| String literals | `"foo"` or `'foo'` | Single quotes only: `'foo'` | Double quotes delimit YAML -- single quotes avoid escaping hell |
| Boolean | `True / False` | `true / false` | YAML-native; no case collision |
| Null | `None` | `null` | YAML-native |
| Time literals | Not native | `24h`, `5min`, `30s` native | Duration is a first-class concept in process modeling |
| Duration comparison | Manual | `elapsed < 4h` native | Reads like English; reduces boilerplate |

### Path Examples

```yaml
entity.risk_score            # Entity attribute
entity.priority              # Enum value
entity.lifecycle             # Current lifecycle state
token.elapsed                # Duration since token created
token.variables.x            # Token-scoped variable
flow.elapsed                 # Duration since flow started
flow.tokens                  # Count of active tokens
metrics.cycle_time.avg       # Average cycle time
metrics.sla_compliance       # Percentage meeting SLA
params.sla_target            # Tunable parameter
```

### Collection Functions

**Filtering:**

| Function | Example |
|----------|---------|
| `where(col, pred)` | `where(tokens, entity.approved == true)` |
| `distinct(col, path)` | `distinct(tokens, entity.reviewer_id)` |

**Counting:**

| Function | Example |
|----------|---------|
| `len(col)` | `len(tokens)` |
| `count(col, pred)` | `count(tokens, entity.risk > 0.7)` |
| `any(col, pred)` | `any(tokens, entity.flagged)` |
| `all(col, pred)` | `all(tokens, entity.approved)` |
| `none(col, pred)` | `none(tokens, entity.rejected)` |

**Aggregation:**

| Function | Example |
|----------|---------|
| `sum(col, path)` | `sum(tokens, entity.amount)` |
| `avg(col, path)` | `avg(tokens, entity.risk_score)` |
| `min(col, path)` | `min(tokens, entity.created_at)` |
| `max(col, path)` | `max(tokens, entity.amount)` |
| `percentile(col, path, p)` | `percentile(tokens, entity.wait_time, 95)` |

**Time-Series:**

| Function | Example |
|----------|---------|
| `rate(metric, window)` | `rate(flow.completed, 1h)` |
| `moving_avg(metric, window)` | `moving_avg(metrics.cycle_time, 24h)` |
| `delta(metric, window)` | `delta(metrics.throughput, 1h)` |
| `trend(metric, window)` | `trend(metrics.sla_compliance, 7d)` |

### Example Expressions

```yaml
# Edge condition
c: "entity.risk_score > 0.7 and entity.amount > 50000"

# Node guard
g: "token.elapsed > 4h and entity.priority == 'vip'"

# Phase gate
evaluate: "metrics.sla_compliance < 0.90 and flow.elapsed > 7d"

# Vocabulary mapping
vocabulary:
  - term: "high-risk"
    maps_to: "entity.risk_score > 0.7"
  - term: "overdue"
    maps_to: "token.elapsed > params.sla_target"
```

---

## Phase Boundaries (Metamorphosis)

A phase boundary is a first-class construct in the Alterverse. It
connects one IR to a different IR entirely -- not a different branch
through the same graph, but a different graph.

```
Regular branch:       IR1 -> IR1 (different path, same graph)
Metamorphic branch:   IR1 -> IR2 (different graph entirely)
```

Identity persists through metamorphosis. Intention transforms. Structure
transforms. Selected state persists.

| Persists | Why |
|----------|-----|
| Entity identity | It is still the same loan, organism, company |
| Intention | Carried explicitly -- may transform |
| Selected variables | Marked persist: true |
| Lineage | Audit trail of what led here |

| Dissolves | Why |
|-----------|-----|
| Graph structure | Being replaced |
| In-flight tokens | Migrate, cancel, or complete per strategy |
| Resource bindings | New structure may need different resources |
| Local variables | Unless marked persistent |

### Phase Boundary Schema

```yaml
phase_boundaries:
  - id: pivot_to_enterprise
    type: metamorphosis

    from:
      ir: "startup_workflow_v1"
      checkpoint: "scale_ready"
      intention: "Find product-market fit"

    to:
      ir: "enterprise_workflow_v1"
      resume_at: "onboarding"
      intention: "Grow and defend revenue"

    persist:
      - entity
      - variables: [customer_base, revenue, team_size]
      - lineage: true

    dissolve:
      - graph
      - tokens
      - resources

    migration: drain      # drain | complete_pending | cancel | migrate | checkpoint
    reversible: true
```

Migration strategies:

| Strategy | Behavior |
|----------|----------|
| `drain` | Stop new arrivals; let existing tokens complete; then swap |
| `complete_pending` | Let all current tokens finish in old graph; then swap |
| `cancel` | Abort in-flight tokens; swap immediately |
| `migrate` | Map old node positions to new graph; move tokens |
| `checkpoint` | Snapshot token states; swap; restore at equivalent positions |

---

## Surrogate Models

A surrogate is an ML model trained on simulation and production runs. It
replaces the DES engine for fast prediction. Simulation is the factory.
The surrogate is the product.

```yaml
surrogates:
  - id: call_center_v3
    type: neural_network    # neural_network | gradient_boost | gaussian_process | ensemble
    trained_on:
      simulation_runs: 10000
      production_window: "2025-01-01 to 2026-01-01"
    inputs:
      - name: queue_depth
        type: number
        range: [0, 200]
      - name: agents_available
        type: number
        range: [0, 250]
    outputs:
      - name: predicted_sla
        type: number
        range: [0, 1]
      - name: recommended_action
        type: enum
        values: [hold, add_staff, reduce_break, activate_cross_trained]
    drift_detection:
      metric: mse
      threshold: 0.05
      window: 1h
      action: alert         # alert | retrain | fallback_to_des
    version: 3
    accuracy:
      mse: 0.023
      r2: 0.94
```

A surrogate can be used directly as an operator:

```yaml
- id: capacity_decision
  t: decision
  mode: exclusive
  o:
    op: surrogate
    model: call_center_v3
```

---

## Multi-Agent Modeling

PRISM-IR processes are the "DNA" of actors. Each actor runs an instance
of a process. An ecosystem is multiple processes running concurrently,
interacting through a shared environment.

Level-of-detail (LOD) is borrowed from video game rendering. In a game,
objects close to the camera render at full resolution. Objects far away
render as blobs, or get skipped entirely. The engine does not waste
compute on things the player cannot see clearly.

PRISM-IR applies the same principle to multi-agent simulation. If you
are simulating a pond with 500 frogs, 20 snakes, and 10,000 flies, you
do not simulate every fly's full lifecycle at full fidelity. The frog
your simulation is focused on runs a complete PRISM-IR process. The
frogs nearest to it run simplified processes. The frogs across the pond
are a statistical approximation. The flies are a carrying-capacity
constant. You get realistic emergent behavior at the focus point without
the compute cost of full fidelity everywhere.

The quality of LOD simulation depends on the accuracy of the statistical
models used for distant zones. PRISM-IR defines the zone structure and
transition rules. The accuracy of the approximations is a domain and
runtime concern -- the spec provides the mechanism, not the models.

Level-of-detail zones:

| Zone | Radius | Modeling Approach |
|------|--------|-------------------|
| Zone 0 | Focus entity | Full PRISM-IR process |
| Zone 1: Immediate | 0-2m | Full actor simulation |
| Zone 2: Local | 2-10m | Simplified actors |
| Zone 3: Distant | 10-50m | Statistical model |
| Zone 4: Background | Beyond | Constants or slow curves |

```yaml
# Multi-agent flow
actors:
  - id: frog_population
    count: 20
    process: frog_lifecycle
    spawn_profile:
      energy: { dist: normal, mean: 70, std: 15 }

environment:
  resources:
    - id: fly_population
      type: population
      model: logistic_growth
      params: { carrying_capacity: 1000, growth_rate: 0.1 }

lod:
  - zone: immediate
    radius: 2m
    actors: full_process
  - zone: local
    radius: 10m
    actors: simplified
  - zone: distant
    radius: 50m
    actors: statistical
```

---

## Domain Vocabularies

Domain vocabularies let PRISM-IR speak the native language of any field
without changing the underlying primitives.

```yaml
# biology.vocab.yaml
domain: biology
extends: prism-ir-core

mappings:
  organism:
    maps_to: entity
    default_attrs: [energy, health, position, reproductive_status]
    lifecycle: [embryo, juvenile, adult, senescent, dead]

  predation:
    maps_to: event
    participants: [predator, prey]
    outcomes: [success, failure, escape]

  mitosis:
    maps_to: node
    type: task
    action: fork_entity

functions:
  fitness: "survival_probability * reproductive_success"
  predation_success: "predator.speed / prey.speed * cover_factor"
```

### Cross-Domain Pattern Library

Many domains share underlying mathematical structures. Starling
murmurations and trader herding follow the same equations. PRISM-IR
captures these as named patterns that domains bind to:

```yaml
# Shared patterns (sample)
patterns:
  - contagion        # Epidemic spread, rumor spread, viral marketing
  - predator_prey    # Ecosystems, market makers vs retail
  - flocking         # Murmurations, crowd behavior, momentum trading
  - phase_transition # Metamorphosis, market regimes, opinion tipping points
  - queuing          # Call centers, order books, traffic
  - logistic         # Population growth, technology adoption
```

```yaml
# biology binds flocking to starlings
murmuration:
  pattern: flocking
  bind:
    entity: starling
    separation_radius: 1m

# finance binds flocking to momentum traders
momentum_crowd:
  pattern: flocking
  bind:
    position: portfolio_weights
    velocity: trading_direction
    neighbors: same_sector_funds
```

A surrogate trained on starling flocking may inform predictions about
trader herding -- the math is the same.

---

## Van der Aalst 43-Pattern Coverage

PRISM-IR covers all 43 workflow patterns from the van der Aalst reference
model (workflowpatterns.com). This is achieved through the node type
system, join policies, and three coordination support role primitives.

| # | Pattern | Covered By |
|---|---------|-----------|
| 1 | Sequence | Edge between nodes |
| 2 | Parallel Split | `t: fork` |
| 3 | Synchronization | `t: join`, `mode: all` |
| 4 | Exclusive Choice | `t: decision`, `mode: exclusive` |
| 5 | Simple Merge | `t: join` |
| 6 | Multi-Choice | `t: decision`, `mode: multi` |
| 7 | Structured Synchronizing Merge | `t: join`, `mode: all`, `structured: true` |
| 8 | Multi-Merge | `t: join`, `mode: multi_merge` |
| 9 | Structured Discriminator | `t: join`, `mode: first_of_m` |
| 10 | Arbitrary Cycles | Back-edge in graph |
| 11 | Implicit Termination | `autoTerminate: true` on flow |
| 12 | MI without Sync | `instance_factory` + resource pool |
| 13 | MI with Design-Time Count | `instances: { count: N }` |
| 14 | MI with Runtime Count | `instances: { count: expr }` |
| 15 | MI without A Priori Runtime Knowledge | `instance_factory` (dynamic) |
| 16 | Deferred Choice | `t: event_wait` (hold until signal) |
| 17 | Interleaved Parallel Routing | `t: join`, `mode: interleaved`, `mutex: true` |
| 18 | Milestone | Edge milestone guard + event condition |
| 19 | Cancel Activity | `t: cancel`, `scope: activity` |
| 20 | Cancel Case | `t: cancel`, `scope: case` |
| 21 | Arbitrary Loops | Back-edge in graph |
| 22 | Recursion | Back-edge with `maxDepth` guard |
| 23 | Transient Trigger | `t: event_wait`, event `type: transient` |
| 24 | Persistent Trigger | `t: event_wait`, event `type: persistent` |
| 25 | Partial Join | `t: join`, `mode: n_of_m` + cancel |
| 26 | Blocking Discriminator | `t: join`, `mode: first_of_m`, `block_others: true` |
| 27 | Canceling Discriminator | `t: join`, `mode: first_of_m`, `cancel_others: true` |
| 28 | N-of-M Join | `t: join`, `mode: n_of_m` |
| 29 | Synchronizing Merge | `t: join`, `mode: all` |
| 30 | Local Synchronizing Merge | `t: join`, `mode: all`, `local: true` |
| 31 | General Synchronizing Merge | `t: join`, `structured: false` |
| 32 | Thread Merge | `t: join` + runtime state reference |
| 33 | Thread Split | `t: fork` + runtime state reference |
| 34 | Static Partial Join | `t: join`, `mode: n_of_m`, `static: true` |
| 35 | Canceling Partial Join | `t: join`, `mode: n_of_m` + `t: cancel` |
| 36 | Multiple Instance Partial Join | `instance_factory` + `t: join`, `mode: n_of_m` |
| 37 | Direct Allocation | Resource pool direct assignment |
| 38 | Role-Based Distribution | Resource pool + skill matching |
| 39 | Deferred Distribution | Resource pool, `deferred: true` |
| 40 | Authorization | `t: task`, `op: human` + approval gate |
| 41 | Separation of Duties | Multiple approvers with distinct roles |
| 42 | Case Handling | Entity lifecycle states |
| 43 | Retain Familiar | Resource pool + ledger history lookup |

**Coverage: 43/43 (100%)**

---

## Complete Example

Loan approval process demonstrating core PRISM-IR features.

```yaml
v: "1.0"
id: "loan_approval_flow"
name: "Loan Approval Process"
domain: "lending"

intention: "Approve loans"
failure_tolerance: "5%"

constraints:
  sla: "95% within 4 hours"
  fail: ">24h"
  priority: "speed > thoroughness"

vocabulary:
  - term: "applicant"
    maps_to: "entity.type == 'loan_application'"
  - term: "high-risk"
    maps_to: "entity.risk_score > 0.7"
  - term: "approved"
    maps_to: "node.decision.outcome == 'approved'"
  - term: "fast-track"
    maps_to: "entity.priority == 'vip'"

entities:
  - type: loan_application
    attrs:
      - { name: applicant_id, dtype: string, required: true }
      - { name: amount,       dtype: number, required: true }
      - { name: risk_score,   dtype: number }
      - { name: priority,     dtype: enum, values: [standard, vip], default: standard }
    lifecycle: [submitted, reviewing, decided, closed]

events:
  - id: evt_fraud_alert
    type: persistent
    payload:
      - { name: alert_level, dtype: number }
  - id: evt_loan_approved
    type: transient
    payload:
      - { name: loan_id,  dtype: string }
      - { name: amount,   dtype: number }

generators:
  - id: loan_arrivals
    entity: loan_application
    arrival:
      distribution: poisson
      rate: 12
    warmup: "5 min"
    schedule: "09:00-17:00 weekdays"

queues:
  - id: main_queue
    discipline: priority
    priority_expr: "entity.priority == 'vip'"
    reneging:
      timeout: "30 min"
      action: escalate

resources:
  - id: senior_reviewers
    capacity: 5
    skills: [high_risk, escalation]
    schedule:
      shifts:
        - name: day
          hours: "09:00-17:00"
          capacity: 5
    dispatch:
      mode: scored
      scoring:
        factors:
          - name: quality
            weight: 100
            expr: "agent.profile.high_risk.sigma"

groups:
  - id: identity_verification
    intention: "Verify identity"
    failure_tolerance: "2 consecutive"
    nodes: [id_check, doc_verify, fraud_scan]

nodes:
  - id: start
    t: start

  - id: risk_assessment
    t: task
    o: { op: llm, tier: 2 }
    tm: { d: lognorm, mean: 30, std: 10 }
    failure_policy:
      retry: 2
      then: failover
      fallback: { op: llm, tier: 3 }
      block_failed_for: "10 min"
      if_all_fail: escalate

  - id: parallel_fork
    t: fork

  - id: review_a
    t: task
    o: { op: human, tier: 4 }

  - id: review_b
    t: task
    o: { op: llm, tier: 3 }

  - id: review_c
    t: task
    o: { op: llm, tier: 3 }

  - id: review_vote
    t: vote
    mode: majority
    verdict_expr: "result.outcome == 'approved'"
    tie_breaker:
      policy: escalate
      operator: { op: human, tier: 4 }
    out:
      approved: final_decision
      rejected: end_rejected
      tie: senior_review

  - id: final_decision
    t: decision
    mode: exclusive
    o: { op: human, tier: 4 }
    out:
      approved: end_approved
      rejected: end_rejected

  - id: end_approved
    t: end
    a:
      - type: emit
        event: evt_loan_approved
        payload:
          loan_id: "${entity.id}"
          amount: "${entity.amount}"

  - id: end_rejected
    t: end

  - id: senior_review
    t: task
    o: { op: human, tier: 4 }

edges:
  - { s: start,           t: risk_assessment }
  - { s: risk_assessment, t: parallel_fork }
  - { s: parallel_fork,   t: review_a }
  - { s: parallel_fork,   t: review_b }
  - { s: parallel_fork,   t: review_c }
  - { s: review_a,        t: review_vote }
  - { s: review_b,        t: review_vote }
  - { s: review_c,        t: review_vote }
  - { s: review_vote,     t: final_decision,  c: "vote.result == 'approved'" }
  - { s: review_vote,     t: end_rejected,    c: "vote.result == 'rejected'" }
  - { s: review_vote,     t: senior_review,   c: "vote.result == 'tie'" }
  - { s: senior_review,   t: final_decision }
  - { s: final_decision,  t: end_approved,    c: "outcome == 'approved'" }
  - { s: final_decision,  t: end_rejected,    c: "outcome == 'rejected'" }

phase_boundaries:
  - id: pivot_to_enterprise
    type: metamorphosis
    from:
      ir: "loan_approval_flow"
      checkpoint: "scale_ready"
      intention: "Approve loans"
    to:
      ir: "enterprise_lending_v1"
      intention: "Optimize and defend lending portfolio"
    persist:
      - entity
      - variables: [customer_base, revenue]
    migration: drain

metrics:
  - cycle_time
  - sla_compliance
  - abandonment_rate
  - reviewer_utilization
```

---

## Key Principles

1. **Humans write English. LLMs write IR.** The intended authorship
   model is English in, PRISM-IR out. Humans work at the intention
   layer. LLMs work at the IR layer.

2. **Intention is first-class.** Without "why," execution is a black box.

3. **Same IR, four modes.** The flow never changes. Only operator
   bindings change.

4. **LLM, human, API, script are interchangeable at the node level.**
   The platform routes, waits, collects, and moves on.

5. **Metamorphosis preserves identity.** The organism is continuous. The
   IR is just its current body.

6. **The Alterverse holds everything.** No branch is deleted. Every
   counterfactual is preserved and queryable.

7. **English -> IR -> English.** If the round-trip loses meaning, the IR
   is wrong. This is LLM-to-LLM fidelity, not human readability.

8. **Complexity arises from need.** A three-node flow is three nodes.
   The full join policy table, failure policies, and resource dispatch
   modes only activate when the process being described actually requires
   them.

9. **The spec defines mechanisms, not models.** PRISM-IR specifies how
   LOD zones work, how surrogates plug in, how statistical approximations
   replace full simulation at distance. The accuracy of those
   approximations is a domain and runtime responsibility, not a spec
   responsibility. TCP/IP does not guarantee the quality of what you send
   over it.

---

## References

- Van der Aalst Workflow Patterns: https://www.workflowpatterns.com/
- BPMN 2.0: OMG standard
- Erlang OTP Supervision Trees: failure policy foundations
- Petri Net formalism: token/place semantics
- SimPy: generator and arrival pattern conventions
- L-Systems: grammar-based growth (biological domain foundation)

---

*PRISM-IR v1.0 -- DEIA Solutions -- deiasolutions.com*
*"Describe your process once. Simulate your intent. Manifest it."*
