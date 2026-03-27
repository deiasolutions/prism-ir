# We Built a Universal Process IR. Here's Why It Matters.

*Published by DEIA Solutions Shiftcenter -- shiftcenter.com*

---

Every organization runs on processes. Loan approvals. Hiring pipelines.
Clinical trials. Supply chains. Ecosystem simulations. Software
deployments. Behind every one of them is a description of how work
moves from intent to outcome.

The problem is that description exists in three incompatible places at
once: in someone's head, in a diagram that went stale six months ago,
and in code that nobody outside engineering can read.

We built PRISM-IR to fix that.

---

## What PRISM-IR Is

PRISM-IR is an open intermediate representation for any process.

**PRISM** stands for Process Representation, Intent Simulation &
Manifestation. The IR is the intermediate representation -- the
normalized form that sits between how you describe a process and how
it actually runs. Think of it as the universal language that lets your
intent travel from a sentence in English all the way to production
execution without getting lost in translation.

The core idea is straightforward: describe a process once, in a single
file, and run it four ways.

- **Simulate it** in virtual time. Run ten thousand branches. Find the
  failure modes before they find your customers.
- **Execute it** in production against real operators -- humans, APIs,
  LLMs, scripts.
- **Run it hybrid** -- some nodes simulated, some real, in the same
  flow.
- **Optimize it** -- let ML learn from simulation and production runs
  and surface the configurations that perform best on the metrics you
  actually care about.

Same file. Same spec. Same intent. No translation between systems, no
seams where meaning gets lost.

---

## Nobody Writes the YAML

Here is the most important thing to understand about PRISM-IR: it is
not a language for humans to write by hand.

Humans describe processes in plain English. LLMs translate that English
into PRISM-IR. Runtimes execute the IR. LLMs reconstruct the English
from the IR on demand. Humans work at the intention layer. LLMs work at
the IR layer.

This is the design. The entire spec -- the expression language, the join
policy tables, the operator schemas, the resource dispatch modes -- is
a precise vocabulary for LLMs to reason about process structure without
ambiguity. It is not a learning curve. It is a contract between LLMs
and runtimes.

A human says:

> "We need to approve employee expenses. A reviewer looks at each claim
> and approves or rejects it. 95% should be decided within 24 hours."

An LLM produces a complete, executable PRISM-IR file. The human never
touches the YAML. They describe their process, review the simulation
results, and decide whether to deploy. That is the entire interaction.

---

## Why Intention Is First-Class

Every process tool we looked at captures what a process does. BPMN
gives you gateways and tasks. Workflow engines give you steps and
transitions. Orchestration frameworks give you nodes and edges.

Nobody captures why.

PRISM-IR requires every process -- and every sub-process within it --
to declare its intention. A verb and an object. "Approve loans."
"Verify identity." "Detect fraud."

This is not a comment. It is a first-class field that the runtime
measures against. When execution completes, the platform can tell you
whether intent matched outcome -- not just whether the process
finished, but whether it finished for the right reason at the right
quality.

Without "why," you can tell a process completed. With it, you can tell
whether it worked.

---

## The Round-Trip Guarantee -- and Fidelity Drift

PRISM-IR is designed so that any LLM, given the IR, can reconstruct
the original process description in English without losing meaning.

English -> IR -> English. If the round-trip fails, the IR is wrong.

This is not a documentation feature. It is an LLM-to-LLM fidelity
test. It means any conforming runtime, any LLM, any tool in the
ecosystem can read a PRISM-IR file and understand what it means -- not
just what it does structurally, but what it is trying to accomplish and
how to measure success.

It is the difference between a file format and a contract.

**IR carries a second meaning that is not accidental.** In the DEIA
Shiftcenter platform, IR also stands for Intent / Result -- the unit of
accountability in every process. A process declares its intent before
it runs. Execution produces a result. The platform measures the
round-trip fidelity between them, scoring what was preserved, what was
lost, and what was hallucinated.

**Fidelity drift** is what happens when ambiguous intent gets resolved
into a specific IR structure. The output looks right. It may even
execute correctly. But it encodes someone's best guess about what you
meant -- not what you meant. Like a transcription error in DNA, it is
silent. The sequence is still valid. It still executes. But it codes
for a slightly different outcome. And it compounds along the chain: a
slightly ambiguous intention at the flow level produces a slightly wrong
group definition, which produces a slightly wrong node behavior, which
produces a measurably wrong result.

**The bidirectional test catches it.**

The standard test is forward: English -> IR -> English. Generate IR
from a description, reconstruct English from the IR using a fresh LLM
with no memory of the original, compare. This catches hallucination at
the encoding step.

The reverse test is new: IR -> English -> IR. Take a PRISM-IR file,
generate English from it with no other context, feed that English to a
second LLM and ask it to produce IR, compare the result to the
original. This catches ambiguity in the natural language layer --
places where the English generated from the IR was not specific enough
for a fresh LLM to reconstruct the same structure.

The two scores together are a diagnostic:

| Forward | Reverse | Diagnosis |
|---------|---------|-----------|
| High | High | Clean. English and IR agree. |
| High | Low | IR is consistent but generates ambiguous English. |
| Low | High | Original English was ambiguous; IR resolved it confidently. Hallucination risk at intake. |
| Low | Low | Both directions leak. Revisit the source description. |

This is why the Simon Willison problem is solvable in a governed
process platform but not in a one-shot LLM interaction. A single
forward pass has no way to know what it hallucinated. A bidirectional
fidelity test does.

---

## One Spec, Every Domain

We did not build PRISM-IR for business workflows. We built it for any
process that can be described in words.

The same IR format that models a loan approval also models a clinical
trial, a frog's lifecycle in a pond ecosystem, a software deployment
pipeline, or the spread of a disease through a population.

Domain vocabularies let PRISM-IR speak the native language of any
field. A biologist describes organisms and predation events. A logistics
engineer describes shipments and handoffs. A financial modeler describes
trades and settlement. The vocabulary layer maps domain terms to
PRISM-IR primitives. The underlying IR -- and the runtime that executes
it -- never changes.

And because many domains share underlying mathematical structures
(starling murmurations and momentum trading follow the same flocking
equations; epidemic spread and viral marketing follow the same
diffusion model), ML models trained in one domain can inform predictions
in another. The pattern library is the transferable knowledge.

---

## The Alterverse

Every branch taken in a simulation creates a timeline. Every production
run creates a timeline. Every counterfactual you choose not to take
creates a timeline.

The Alterverse is the tree of all of them.

Nothing is deleted. Every path -- the ones taken, the ones rejected,
the ones you ran in simulation before deciding -- is preserved and
queryable. This is what makes PRISM-IR genuinely useful for governance
and auditability. It is not enough to know what decision was made. You
need to know what alternatives existed, what the simulation predicted,
and whether the prediction matched reality.

The Alterverse is that audit trail, at every level of every process,
across every timeline.

---

## 43/43

The van der Aalst workflow pattern reference model is the most
comprehensive formal taxonomy of process patterns that exists. Forty-
three patterns covering every known control-flow structure in industrial
workflow systems.

PRISM-IR covers all forty-three. Not aspirationally. Verified, with a
coverage table in the spec mapping each pattern to the IR construct that
implements it.

This matters because it means PRISM-IR is not a toy. Any process that
has ever been formally modeled can be expressed in PRISM-IR. Any process
that can be expressed in BPMN, Petri nets, or workflow YAML can be
compiled into PRISM-IR without loss.

---

## Open Spec, Proprietary Runtime

The PRISM-IR specification is published today under the Apache 2.0
license at github.com/deiasolutions/prism-ir.

The spec is the contract. The runtime -- the simulation engine,
production executor, event ledger, surrogate pipeline, and Alterverse
query layer -- is what DEIA Solutions Shiftcenter builds and operates.

We are making the spec open because interoperability requires a public
contract. If PRISM-IR is going to become the universal process IR we
believe it can be, it needs to be something anyone can build against,
validate against, and extend for their domain. Keeping the spec
proprietary would make it a vendor format. Making it open makes it
infrastructure.

The value of what we build is not in the format. It is in what runs on
top of it.

---

## What PRISM-IR Does Not Guarantee

Simon Willison recently published a careful experiment: he asked an AI
to decompile a 39KB Turbo Pascal executable. The output looked
expert-level. Seventeen segments mapped. Detailed assembly annotations.
A second AI model verified the output before publication. Then a real
assembly programmer compared the annotations to the actual binary.
Roughly half were wholesale fabrication -- invented instructions with
plausible-sounding labels, seamlessly blended with genuine analysis.
Two AI models. One of the most careful AI practitioners alive. None of
them caught it.

Hallucinations do not sound wrong anymore. They sound like expertise
you would have no reason to doubt.

This is directly relevant to PRISM-IR, and we want to be honest about
where the spec protects you and where it does not.

**Where PRISM-IR protects you:**

The round-trip guarantee catches semantic drift at the IR layer. If an
LLM generates an IR structure that cannot reconstruct the original
English intent without loss, the fidelity check fails and the IR is
rejected. The expression language is constrained and validatable --
hallucinated paths that do not exist in the schema fail the parser.
Syntactically invalid IR is caught before execution.

**Where PRISM-IR does not protect you:**

The Simon Willison problem is subtler. The hallucinated annotations
were syntactically valid and semantically plausible. They fit the
pattern of correct output well enough that two verification passes
missed them.

In PRISM-IR terms: an LLM could generate a flow that is syntactically
valid, passes the round-trip, and covers all declared intentions --
and still model the wrong process. If the human's English description
was ambiguous, the LLM's interpretation was confident, and the
round-trip reconstructs the LLM's interpretation faithfully, you have
a process that runs correctly but does not do what the human actually
meant. The round-trip catches IR corruption. It does not catch intent
corruption at the source.

**The answer is Tabletop mode.**

PRISM-IR's Tabletop execution mode walks a process step by step with
an LLM guide before any simulation or production run begins. At each
node, the human can verify that the LLM's interpretation matches their
intent. This is not a debugging tool -- it is the primary defense
against confident hallucination at the intent layer. Simulate before
you execute. Walk before you simulate.

The right mental model: PRISM-IR gives you a wind tunnel. A wind tunnel
does not guarantee your design is correct. It guarantees that what you
test is actually what you built, and that the results are real. The
quality of what you put in is still your responsibility.

We are naming this limitation explicitly because Simon Willison got
credit for transparency. We want the same standard to apply here.

---

## What's Next

Today is flag-planting. The spec is v1.0. The runtime is in active
development.

If you are building a workflow engine, an LLM orchestration layer, a
simulation platform, or any system that needs to describe and execute
processes -- read the spec. Build against it. Tell us what is missing.

If you want to be notified when the runtime ships: shiftcenter.com.

---

*DEIA Solutions Shiftcenter*
*"Describe your process once. Simulate your intent. Manifest it."*
*github.com/deiasolutions/prism-ir*
