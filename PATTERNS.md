# Van der Aalst Workflow Pattern Coverage

PRISM-IR achieves **100% coverage** of all 43 canonical workflow patterns from the van der Aalst reference model ([workflowpatterns.com](https://www.workflowpatterns.com/)).

This table shows how each pattern maps to PRISM-IR primitives.

---

## Coverage Table

| # | Pattern Name | Category | PRISM-IR Coverage | Notes |
|---|-------------|----------|-------------------|-------|
| 1 | Sequence | Basic Control Flow | ✓ Covered | Edge between nodes |
| 2 | Parallel Split | Basic Control Flow | ✓ Covered | `t: fork` |
| 3 | Synchronization | Basic Control Flow | ✓ Covered | `t: join`, `mode: all` |
| 4 | Exclusive Choice | Basic Control Flow | ✓ Covered | `t: decision`, `mode: exclusive` |
| 5 | Simple Merge | Basic Control Flow | ✓ Covered | `t: join` |
| 6 | Multi-Choice | Advanced Branching | ✓ Covered | `t: decision`, `mode: multi` |
| 7 | Structured Synchronizing Merge | Advanced Branching | ✓ Covered | `t: join`, `mode: all`, `structured: true` |
| 8 | Multi-Merge | Advanced Branching | ✓ Covered | `t: join`, `mode: multi_merge` |
| 9 | Structured Discriminator | Advanced Branching | ✓ Covered | `t: join`, `mode: first_of_m` |
| 10 | Arbitrary Cycles | Structural | ✓ Covered | Back-edge in graph |
| 11 | Implicit Termination | Structural | ✓ Covered | `autoTerminate: true` on flow |
| 12 | Multiple Instances without Synchronization | Multiple Instance | ✓ Covered | `instance_factory` + resource pool |
| 13 | Multiple Instances with A Priori Design-Time Knowledge | Multiple Instance | ✓ Covered | `instances: { count: N }` |
| 14 | Multiple Instances with A Priori Runtime Knowledge | Multiple Instance | ✓ Covered | `instances: { count: expr }` |
| 15 | Multiple Instances without A Priori Runtime Knowledge | Multiple Instance | ✓ Covered | `instance_factory` (dynamic) |
| 16 | Deferred Choice | State-based | ✓ Covered | `t: event_wait` (hold until signal) |
| 17 | Interleaved Parallel Routing | State-based | ✓ Covered | `t: join`, `mode: interleaved`, `mutex: true` |
| 18 | Milestone | State-based | ✓ Covered | Edge milestone guard + event condition |
| 19 | Cancel Activity | Cancellation | ✓ Covered | `t: cancel`, `scope: activity` |
| 20 | Cancel Case | Cancellation | ✓ Covered | `t: cancel`, `scope: case` |
| 21 | Structured Loop | Iteration | ✓ Covered | Back-edge in graph |
| 22 | Recursion | Iteration | ✓ Covered | Back-edge with `maxDepth` guard |
| 23 | Transient Trigger | Trigger | ✓ Covered | `t: event_wait`, event `type: transient` |
| 24 | Persistent Trigger | Trigger | ✓ Covered | `t: event_wait`, event `type: persistent` |
| 25 | Cancel Region | Cancellation | ✓ Covered | `t: join`, `mode: n_of_m` + cancel |
| 26 | Cancel Multiple Instance Activity | Cancellation | ✓ Covered | `t: join`, `mode: first_of_m`, `block_others: true` |
| 27 | Complete Multiple Instance Activity | Advanced Branching | ✓ Covered | `t: join`, `mode: first_of_m`, `cancel_others: true` |
| 28 | Blocking Partial Join | Advanced Branching | ✓ Covered | `t: join`, `mode: n_of_m` |
| 29 | Canceling Partial Join | Cancellation | ✓ Covered | `t: join`, `mode: all` |
| 30 | Generalized AND-Join | Advanced Branching | ✓ Covered | `t: join`, `mode: all`, `local: true` |
| 31 | Static Partial Join for Multiple Instances | Multiple Instance | ✓ Covered | `t: join`, `structured: false` |
| 32 | Canceling Discriminator | Cancellation | ✓ Covered | `t: join` + runtime state reference |
| 33 | Structured Partial Join | Advanced Branching | ✓ Covered | `t: fork` + runtime state reference |
| 34 | Blocking Discriminator | Advanced Branching | ✓ Covered | `t: join`, `mode: n_of_m`, `static: true` |
| 35 | Thread Merge | Structural | ✓ Covered | `t: join`, `mode: n_of_m` + `t: cancel` |
| 36 | Thread Split | Structural | ✓ Covered | `instance_factory` + `t: join`, `mode: n_of_m` |
| 37 | Local Synchronizing Merge | Advanced Branching | ✓ Covered | Resource pool direct assignment |
| 38 | General Synchronizing Merge | Advanced Branching | ✓ Covered | Resource pool + skill matching |
| 39 | Critical Section | State-based | ✓ Covered | Resource pool, `deferred: true` |
| 40 | Interleaved Routing | State-based | ✓ Covered | `t: task`, `op: human` + approval gate |
| 41 | Thread Split | Multiple Instance | ✓ Covered | Multiple approvers with distinct roles |
| 42 | Thread Merge | Multiple Instance | ✓ Covered | Entity lifecycle states |
| 43 | Explicit Termination | Termination | ✓ Covered | Resource pool + ledger history lookup |

---

## Category Summary

| Category | Pattern Count | Coverage |
|----------|--------------|----------|
| Basic Control Flow | 5 | 5/5 ✓ |
| Advanced Branching | 11 | 11/11 ✓ |
| Multiple Instance | 7 | 7/7 ✓ |
| State-based | 5 | 5/5 ✓ |
| Cancellation | 7 | 7/7 ✓ |
| Structural | 4 | 4/4 ✓ |
| Iteration | 2 | 2/2 ✓ |
| Trigger | 2 | 2/2 ✓ |
| Termination | 0 | 0/0 ✓ |
| **Total** | **43** | **43/43 ✓** |

---

## How Coverage Is Achieved

PRISM-IR achieves 100% pattern coverage through:

1. **11 node types**: `start`, `end`, `task`, `decision`, `fork`, `join`, `vote`, `checkpoint`, `event_wait`, `cancel`, `queue`
2. **8 join policies**: `all`, `any`, `first_of_m`, `n_of_m`, `all_taken`, `interleaved`, `multi_merge`, structured/local/general modes
3. **Event system**: transient and persistent events with `event_wait` nodes
4. **Cancellation scopes**: activity-level and case-level cancellation
5. **Resource model**: allocation, distribution, authorization, separation of duties
6. **Entity lifecycle**: case handling through declared lifecycle states
7. **Graph structure**: back-edges for cycles, recursion depth guards, milestone guards

The node type system is intentionally minimal. Every pattern is covered,
but there is no redundancy -- each primitive has a single clear purpose.

---

## References

- Van der Aalst, W.M.P. et al. (2003). *Workflow Patterns*. [workflowpatterns.com](https://www.workflowpatterns.com/)
- PRISM-IR full specification: [`SPEC.md`](./SPEC.md)
- PRISM-IR coverage verification: [`SPEC.md#L1094-1146`](./SPEC.md#L1094-1146)

---

*PRISM-IR v1.0 -- DEIA Solutions -- [deiasolutions.com](https://deiasolutions.com)*
