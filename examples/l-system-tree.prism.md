---
prism: l-system-tree
version: 1.0.0
---

# L-System Tree

A Lindenmayer-system tree-drawing process expressed as PRISM-IR. The
process iteratively rewrites a string using production rules, then
interprets the resulting string as turtle-graphics commands to draw a
fractal tree. This example demonstrates that PRISM-IR can describe
generative grammars, not just business workflows or biological models.

The same IR shape that drives a claims-processing flow drives the
recursive expansion of an L-system. The primitives transfer.

## Natural Language

A tree-drawing L-system starts with a single axiom (a starting string),
then applies production rules to rewrite the string a fixed number of
times. Each iteration replaces every matching symbol in the string with
its expansion, so the string grows exponentially. After the rewrite
phase, each character in the final string is interpreted as a turtle
command: F means draw a line forward, the plus and minus symbols turn
the turtle by a fixed angle, and the bracket symbols save and restore
the turtle's position so branches can fork off and return. The result
is a self-similar fractal tree.

## PRISM-IR

```yaml
v: "1.0"
id: "l_system_tree"
name: "L-System Tree"
domain: "generative_grammar"

intention: "Expand an L-system axiom and render it as a tree"
failure_tolerance: "any"

vocabulary:
  - term: "axiom"
    maps_to: "entity.string"
  - term: "iteration"
    maps_to: "entity.iteration"
  - term: "fully-expanded"
    maps_to: "entity.iteration >= params.max_iterations"

entities:
  - type: l_system_state
    attrs:
      - { name: string,    dtype: string, required: true }
      - { name: iteration, dtype: number, default: 0 }
    lifecycle: [seeded, expanding, rendering, complete]

events:
  - id: evt_iteration_done
    type: persistent
    payload:
      - { name: iteration,    dtype: number }
      - { name: string_length, dtype: number }

  - id: evt_render_complete
    type: persistent
    payload:
      - { name: drawn_segments, dtype: number }

nodes:
  - id: start
    t: start

  - id: seed
    t: task
    o: { op: script }
    intention: "Initialize the L-system with the starting axiom"
    a:
      - type: set
        path: "entity.string"
        value: "${params.axiom}"
      - type: set
        path: "entity.iteration"
        value: 0

  - id: expansion_check
    t: decision
    mode: exclusive
    out:
      expand: rewrite
      done:   render

  - id: rewrite
    t: task
    o: { op: script }
    intention: "Apply production rules to rewrite each symbol in the string"
    a:
      - type: set
        path: "entity.string"
        value: "${apply_rules(entity.string, params.rules)}"
      - type: set
        path: "entity.iteration"
        value: "${entity.iteration + 1}"
      - type: emit
        event: evt_iteration_done
        payload:
          iteration:    "${entity.iteration}"
          string_length: "${len(entity.string)}"

  - id: render
    t: task
    o: { op: script }
    intention: "Interpret the expanded string as turtle commands and draw the tree"
    a:
      - type: emit
        event: evt_render_complete
        payload:
          drawn_segments: "${count_forward_commands(entity.string)}"

  - id: end
    t: end

edges:
  - { s: start,            t: seed }
  - { s: seed,             t: expansion_check }
  - { s: expansion_check,  t: rewrite, c: "entity.iteration < params.max_iterations" }
  - { s: expansion_check,  t: render,  c: "entity.iteration >= params.max_iterations" }
  - { s: rewrite,          t: expansion_check }
  - { s: render,           t: end }

metrics:
  - final_string_length
  - iterations_completed
  - segments_drawn

params:
  axiom: "F"
  rules:
    F: "FF+[+F-F-F]-[-F+F+F]"
  angle_degrees: 22.5
  max_iterations: 4
  segment_length: 5
```
