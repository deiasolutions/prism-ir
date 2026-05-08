---
prism: sir-epidemic
version: 1.0.0
---

# SIR Epidemic Model

A classical compartmental epidemic model rendered as a PRISM-IR process.
This example demonstrates that PRISM-IR is domain-agnostic: the same IR
machinery that describes a business workflow describes the lifecycle of
an organism in an epidemic.

## Natural Language

Each individual in a population is in one of three states: susceptible,
infected, or recovered. Susceptible individuals become infected through
contact with infected individuals at a contact rate that depends on how
many infected people they encounter. Infected individuals recover after
an average duration determined by the disease, transitioning to the
recovered state. Recovered individuals do not become susceptible again
in this model. The simulation tracks how many individuals are in each
state over time and the peak infection level reached.

## PRISM-IR

```yaml
v: "1.0"
id: "sir_epidemic"
name: "SIR Epidemic Model"
domain: "epidemiology"

intention: "Model disease spread through a population"
failure_tolerance: "unlimited"

vocabulary:
  - term: "susceptible"
    maps_to: "entity.state == 'S'"
  - term: "infected"
    maps_to: "entity.state == 'I'"
  - term: "recovered"
    maps_to: "entity.state == 'R'"
  - term: "contact"
    maps_to: "evt_contact"

entities:
  - type: individual
    attrs:
      - { name: person_id, dtype: string, required: true }
      - { name: state,     dtype: enum, values: [S, I, R], default: S }
      - { name: infected_at, dtype: number, default: null }
    lifecycle: [S, I, R]

events:
  - id: evt_contact
    type: transient
    payload:
      - { name: source_id, dtype: string }
      - { name: target_id, dtype: string }

  - id: evt_infection
    type: persistent
    payload:
      - { name: person_id, dtype: string }
      - { name: at,        dtype: number }

  - id: evt_recovery
    type: persistent
    payload:
      - { name: person_id, dtype: string }
      - { name: duration,  dtype: number }

generators:
  - id: contact_events
    entity: individual
    arrival:
      distribution: poisson
      rate: 100

nodes:
  - id: start
    t: start

  - id: susceptible_state
    t: task
    o: { op: script }
    intention: "Hold individual in susceptible state until contact"

  - id: contact_check
    t: event_wait
    trigger:
      event: evt_contact

  - id: infection_decision
    t: decision
    mode: exclusive
    out:
      infected:    infected_state
      not_infected: susceptible_state

  - id: infected_state
    t: task
    o: { op: script }
    intention: "Track infected individual through recovery period"
    a:
      - type: set
        path: "entity.state"
        value: "I"
      - type: set
        path: "entity.infected_at"
        value: "${now}"
      - type: emit
        event: evt_infection
        payload:
          person_id: "${entity.person_id}"
          at: "${now}"

  - id: recovery_timer
    t: task
    o: { op: script }
    tm: { d: lognorm, mean: 14, std: 3 }
    intention: "Wait the disease-specific recovery duration"

  - id: recovered_state
    t: task
    o: { op: script }
    intention: "Transition individual to recovered state"
    a:
      - type: set
        path: "entity.state"
        value: "R"
      - type: emit
        event: evt_recovery
        payload:
          person_id: "${entity.person_id}"
          duration:  "${now - entity.infected_at}"

  - id: end_recovered
    t: end

edges:
  - { s: start,              t: susceptible_state }
  - { s: susceptible_state,  t: contact_check }
  - { s: contact_check,      t: infection_decision }
  - { s: infection_decision, t: infected_state,    c: "random() < params.infection_probability" }
  - { s: infection_decision, t: susceptible_state, c: "random() >= params.infection_probability" }
  - { s: infected_state,     t: recovery_timer }
  - { s: recovery_timer,     t: recovered_state }
  - { s: recovered_state,    t: end_recovered }

metrics:
  - infected_count
  - peak_infected
  - r_zero
  - epidemic_duration

params:
  infection_probability: 0.15
  population_size: 10000
```
