# PRISM-IR

**Process Representation, Intent Simulation & Manifestation.**

*Describe your process once. Simulate your intent. Manifest it.*

PRISM-IR is the source language for declarative process programs. Humans describe processes in plain English. LLMs write the program. Conforming runtimes execute it. Other LLMs reconstruct English from it on demand. **You never touch the YAML.**

The language sits between input (English, BPMN, L-systems, other domain formats) and execution engines (simulation, production, optimizer). It is read and written by LLMs, not by humans directly.

## Status

- **Current version:** v1.1.0 — additive amendments for 8OS compatibility ([`SPEC-v1.1.md`](./SPEC-v1.1.md)).
- **Baseline:** v1.0.0 ([`SPEC.md`](./SPEC.md)).
- **Pattern coverage:** [43 of 43 van der Aalst Workflow Patterns](./PATTERNS.md). The full canonical reference set is expressible.
- **Runtime model:** language-spec-only by design. Runtimes are pluggable; the [reference runtime is 8OS](https://github.com/deiasolutions/8os).

## Why PRISM-IR

Most process tools force a choice between simulation and production — different tools, different formats, different data. The seams between them are where meaning gets lost. PRISM-IR eliminates the seams. One program runs everywhere; simulation and production share the same graph, schema, and event ledger.

Three properties no other format combines:

- **Intention is first-class.** Every program — and every sub-process — declares why it exists, not just what it does. Without "why," a process is a black box.
- **Round-trip fidelity.** English → IR → English. The IR must preserve intent under round-trip. If the regenerated English drifts from the original intent, the program is wrong.
- **Operators are interchangeable.** At the node level, an LLM, a human, an API, and a script are interchangeable. Swap one for another without changing the program. Route by cost, quality, availability, or governance.

## Four execution modes

One PRISM-IR program. Four execution modes:

| Mode | What happens |
|---|---|
| **Simulation** | Run in virtual time. Explore branches. Find failure modes before they happen. |
| **Production** | Execute against real operators: humans, APIs, LLMs, scripts. |
| **Hybrid** | Mix simulation and production in the same flow. |
| **Optimization** | ML learns from runs. Returns Pareto-optimal configurations. |

## Composition witnesses

Three demonstrations of PRISM-IR programs hosted by the [8OS reference runtime](https://github.com/deiasolutions/8os). See the [8OS overview](https://github.com/deiasolutions/8os/blob/main/docs/8OS-OVERVIEW-v3.md) for the runtime's framing of all three:

- **[`lsystem-demo`](https://github.com/deiasolutions/lsystem-demo)** — a Level-1 PRISM-IR program declaring an L-system rule-rewriting workflow. 8OS hosts the program; a deterministic decomposer materializes it; a browser-driven adapter renders the result.
- **[SCAN dogfood](https://github.com/deiasolutions/8os/blob/main/docs/demos/scan.md)** — a PRISM-IR program decomposed by an LLM, with real HTTP fetches against live sites, producing a daily-briefing artifact.
- **[`decomposition-strategy-demo`](https://github.com/deiasolutions/decomposition-strategy-demo)** — a PRISM-IR program whose resolution is more PRISM-IR programs that the same runtime then runs. Self-composition.

Three different decomposer fills (deterministic / LLM / program-authored). Three different outside-call profiles. The same source language across all three.

## Key features

- **Four-vector resource profiles.** Resources carry statistical profiles across σ (Quality), π (Preference), α (Autonomy), ρ (Reliability) — per skill, with correlations. Simulation samples from real distributions, not flat averages.
- **Phase boundaries (metamorphosis).** A program can transform into a different program while preserving entity identity, selected state, and lineage. A startup workflow becomes an enterprise workflow. The Alterverse holds every branch of every timeline.
- **Domain vocabularies.** Each domain — biology, finance, logistics, epidemiology — gets a vocabulary layer mapping domain terms to PRISM-IR primitives. The underlying language stays the same. Surrogates trained in one domain can inform predictions in another when the underlying mathematical pattern is shared.
- **Surrogate models as operators.** Train an ML model on simulation and production runs. Plug it back as an operator. Get 1000× faster predictions without re-running the full engine.
- **Multi-agent modeling with level-of-detail.** Run ecosystems of concurrent processes. LOD zones apply full fidelity near the focus entity and statistical approximations at distance — the same technique that makes open-world games tractable.

## File format

Standalone PRISM-IR programs use the `.prism.md` extension. YAML frontmatter identifies the file and version; the program lives in a YAML fenced block in the body. Conforming runtimes may also support PRISM-IR as an embedded block within their own package formats.

## Specification

- [`SPEC-v1.1.md`](./SPEC-v1.1.md) — current language specification.
- [`SPEC.md`](./SPEC.md) — v1.0.0 baseline, preserved.
- [`PATTERNS.md`](./PATTERNS.md) — van der Aalst pattern coverage table.

The spec covers:

- Top-level schema; node types and join policies; vote nodes with majority/unanimous/threshold resolution; operator types and oracle tier routing.
- Token and entity model; event declaration and emission rules; generators and queues.
- Four-vector resource model with statistical profiles and dispatch modes; expression language grammar, namespace, and collection functions.
- Phase boundaries and metamorphosis; surrogate model schema; multi-agent modeling and LOD zones; domain vocabulary format; cross-domain pattern library.
- A complete annotated example.

## Dialect compilers

PRISM-IR can compile to multiple target formats:

| Target | Use case |
|---|---|
| BPMN 2.0 | Business process engines |
| SBML | Systems biology modeling |
| L-systems | Grammar-based growth models |
| Workflow YAML | Generic orchestration engines |

**Specification and schema: open (Apache 2.0).** Anyone can build a conforming runtime or compiler — interoperability requires a public language.

**Dialect compiler implementation: proprietary.** The translation engine is available through the DEIA platform at [deiasolutions.com](https://deiasolutions.com). The platform's value is in the execution engine, optimizer, surrogate pipeline, event ledger, and Alterverse query layer — not in keeping the language secret.

## Principles

1. Humans write English. LLMs write IR.
2. Intention is first-class. Without "why," execution is a black box.
3. Same program, four modes. The flow never changes; only operator bindings change.
4. LLM, human, API, script are interchangeable at the node level.
5. Metamorphosis preserves identity. The organism is continuous; the IR is its current body.
6. The Alterverse holds everything. No branch is deleted; every counterfactual is preserved.
7. English → IR → English. If the round-trip loses meaning, the program is wrong.
8. Complexity arises from need. A three-node flow is three nodes.

## License

The PRISM-IR specification is published under the Apache 2.0 license. See [`LICENSE`](./LICENSE).

---

*DEIA Solutions / [deiasolutions.com](https://deiasolutions.com)*
*"Describe your process once. Simulate your intent. Manifest it."*
