# PRISM-IR errata

## v1.0.1 (2026-11-14)

Corrections to v1.0 material that contradicted itself. No language rule changes: each fix makes an example or a test agree with rules v1.0 already states.

| Where | Defect | Fix |
| --- | --- | --- |
| `tests.yaml` T-020 ("All valid node types present") | Expected a flow to be valid while nine of its eleven nodes had no path from `start`. T-052 rejects a single unreachable node (`UNREACHABLE_NODE`). | The nodes are wired into one reachable flow: `work` → exclusive `branch` → (`split` → `approval` and `wait` → `merge` → `gate`) or `abort` → `end`. Every node type is still exercised. |
| `SPEC.md` Complete Example | The group `identity_verification` named members `id_check`, `doc_verify` and `fraud_scan`, and the phase boundary named checkpoint `scale_ready`. None of them were nodes. | The three identity tasks are added before `risk_assessment`, and `scale_ready` is a checkpoint on the approved path, before `end_approved`. |

Found by the PRISM-IR v1.2 test ladder (rung 2.5, compatibility), which validates every v1.0 file under v1.0 and under v1.2.
