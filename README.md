# PRISM-IR

**Process Representation, Intent Simulation & Manifestation**

Describe your process once. Simulate your intent. Manifest it.

---

## What Is PRISM-IR?

PRISM-IR is a domain-agnostic intermediate representation for any
process -- business workflow, biological system, multi-agent ecosystem,
or anything else that can be described in words.

**Humans describe processes in plain English. LLMs write the IR.
Runtimes execute it. LLMs reconstruct English from it on demand.
You never touch the YAML.**

PRISM-IR is the contract between human intent and machine execution.
It sits between input (English, BPMN, L-systems, and other domain
formats) and execution engines (simulation, production, optimizer).
It is written and read by LLMs, not by humans directly.

---

## Four Execution Modes

One PRISM-IR file. Four execution modes. Same spec, same intent, same
measurement.

| Mode | What Happens |
|------|-------------|
| **Simulation** | Run in virtual time. Explore branches. Find failure modes before they happen. |
| **Production** | Execute against real operators: humans, APIs, LLMs, scripts. |
| **Hybrid** | Mix simulation and production in the same flow. |
| **Optimization** | ML learns from runs. Returns Pareto-optimal configurations. |

---

## PRISM-IR Within the WIRE Framework

PRISM-IR is the **IR layer** of the WIRE framework:

| Layer | What It Is |
|-------|-----------|
| **W**iki | Natural language process descriptions (English) |
| **I**R | Intermediate representation (PRISM-IR) |
| **R**esult | Execution traces, metrics, event ledger |
| **E**xecutable | Compiled dialects (BPMN, SBML, Terraform, etc.) |

The WIRE framework is how DEIA treats processes as living documents:
- **Wiki** is the human intention layer -- plain English descriptions
- **IR** is the canonical source of truth -- LLM-authored PRISM-IR
- **Result** is the measurement layer -- did execution match intent?
- **Executable** is the deployment layer -- dialect-specific compilation

PRISM-IR sits at the center. It translates Wiki into Result. It compiles
into Executable formats. It measures IRD (Intention/Reaction Density) --
the ratio of intentional design to reactive patches. It enforces IRE
fidelity: **Intention → Result → Executable** as the quality gate.

---

## Why PRISM-IR?

Every serious process tool today makes you choose: simulate *or* execute.
Different tools, different formats, different data. You simulate in one
system, build in another, measure in a third. The seams between them are
where meaning gets lost.

PRISM-IR eliminates the seams. One spec runs everywhere. Simulation and
production share the same graph, the same schema, the same event ledger.
You can query a simulation run and a production run in the same dashboard
with the same filters.

Three things nobody else does:

**1. Intention is first-class.**
Every process -- and every sub-process -- declares why it exists. Not
just what it does. The platform measures whether execution matched intent.
Without "why," a process is a black box.

**2. The round-trip guarantee.**
English -> IR -> English. This is not a documentation feature -- it is
an LLM-to-LLM fidelity test. Any LLM that receives a PRISM-IR file must
be able to reconstruct the original intent accurately without loss. If
the round-trip fails, the IR is wrong.

**3. LLM, human, API, script are interchangeable.**
At the node level, PRISM-IR does not care who executes. An LLM and a
human are both operators. Swap one for the other without changing the
flow definition. Route based on cost, quality, availability, or
governance policy.

---

## Quick Example

A human says:

> "We need to approve employee expenses. A reviewer looks at each claim
> and approves or rejects it. 95% should be decided within 24 hours."

An LLM produces:

```yaml
v: "1.0"
id: "expense_approval"
name: "Expense Approval"

intention: "Approve employee expenses"
failure_tolerance: "any"

constraints:
  sla: "95% within 24 hours"

entities:
  - type: expense_claim
    attrs:
      - { name: employee_id, dtype: string, required: true }
      - { name: amount,      dtype: number, required: true }
      - { name: category,    dtype: string }
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

The human described the process in one sentence. The LLM produced the
IR. The same file runs as a simulation to tune staffing, deploys to
production with real reviewers, or swaps the human operator for an LLM
to test automated review. The spec does not change. The human never
touched the YAML.

---

## Key Features

**100% van der Aalst workflow pattern coverage (43/43).**
Every canonical workflow pattern from the van der Aalst reference model --
from simple sequences to multi-instance dynamic parallelism, deferred
choices, and canceling discriminators -- is expressible in PRISM-IR.
See [`PATTERNS.md`](./PATTERNS.md) for the full coverage table.

**Four-vector resource profiles.**
Resources carry statistical profiles across four vectors: Quality (σ),
Preference (π), Autonomy (α), Reliability (ρ). Per skill. With
correlations. Simulation samples from the real distribution of your
workforce, not a flat average.

**Phase boundaries (metamorphosis).**
A process can transform into a completely different process while
preserving entity identity, selected state, and lineage. A startup
workflow becomes an enterprise workflow. A caterpillar becomes a
butterfly. The Alterverse holds every branch of every timeline.

**Domain vocabularies.**
PRISM-IR speaks any domain's native language. Biology, finance,
logistics, epidemiology -- each gets a vocabulary layer that maps domain
terms to PRISM-IR primitives. The underlying IR is always the same.
Surrogates trained in one domain can inform predictions in another when
the underlying mathematical pattern is shared.

**Surrogate models as operators.**
Train an ML model on simulation and production runs. Plug it back in as
an operator. Get 1000x faster predictions without re-running the full
simulation engine.

**Multi-agent modeling with level-of-detail.**
Run ecosystems of concurrent processes. Use level-of-detail (LOD) zones
to apply full simulation fidelity near the focus entity and statistical
approximations at distance -- the same technique that makes open-world
video games tractable.

---

## File Format

Standalone PRISM-IR files use the `.prism.md` extension:

```
my-flow.prism.md
```

YAML frontmatter identifies the file and version. The flow definition
lives in a YAML fenced block in the body. Conforming runtimes may also
support PRISM-IR as an embedded block type within their own package
formats.

---

## Spec and Patterns

The full specification is in [`SPEC.md`](./SPEC.md).
Van der Aalst pattern coverage table is in [`PATTERNS.md`](./PATTERNS.md).

The spec covers:

- Complete top-level schema
- All node types and join policies
- Vote node with majority/unanimous/threshold resolution
- Operator types and oracle tier routing
- Token and entity model
- Event declaration and emission rules
- Generator and queue primitives
- Four-vector resource model with statistical profiles and dispatch modes
- Expression language grammar, namespace, and collection functions
- Phase boundaries and metamorphosis
- Surrogate model schema
- Multi-agent modeling and LOD zones
- Domain vocabulary format
- Cross-domain pattern library
- Complete annotated example

---

## Dialect Compilers and Proprietary vs. Open

**PRISM-IR specification and schema: open (Apache 2.0).**
**Dialect compiler implementation: proprietary.**

PRISM-IR can compile to multiple target formats:

| Target Dialect | Use Case |
|---------------|----------|
| BPMN 2.0 | Business process engines |
| SBML | Systems biology modeling |
| L-systems | Grammar-based growth models |
| Workflow YAML | Generic orchestration engines |
| Terraform | Infrastructure as code |
| Makefile | Build pipelines |

The specification and schema are open because interoperability requires a
public contract. The dialect compiler (the translation engine that
converts PRISM-IR into BPMN, SBML, etc.) is proprietary and available
through the DEIA platform at [deiasolutions.com](https://deiasolutions.com).

Anyone can build a conforming PRISM-IR runtime or compiler. The value of
the DEIA platform is not in keeping the format secret -- it is in the
execution engine, optimizer, surrogate pipeline, event ledger, and
Alterverse query layer that run on top of it.

---

## Principles

1. Humans write English. LLMs write IR.
2. Intention is first-class. Without "why," execution is a black box.
3. Same IR, four modes. The flow never changes. Only operator bindings change.
4. LLM, human, API, script are interchangeable at the node level.
5. Metamorphosis preserves identity. The organism is continuous. The IR is just its current body.
6. The Alterverse holds everything. No branch is deleted. Every counterfactual is preserved.
7. English -> IR -> English. If the round-trip loses meaning, the IR is wrong.
8. Complexity arises from need. A three-node flow is three nodes.

---

## License

The PRISM-IR specification is published under the Apache 2.0 license.

---

*DEIA Solutions / [deiasolutions.com](https://deiasolutions.com)*
*"Describe your process once. Simulate your intent. Manifest it."*
