# Eval card — LogiX-VN refund agent

## Evaluation identity

- **Eval set:** v1, 14 items × 5 fixed seeds (11, 22, 33, 44, 55), sourced from `lab8_public`.
- **Eval-set SHA:** `c9b66b3c6276`.
- **Metric spec:** v1.0, `src/config/metric_spec.yaml`.
- **Harness:** `python -m lab9.eval`, MockLLM, offline; no API key or live customer data.
- **Reports:** baseline `E-swarm-20261117-c9b6`; fixed `E-fixed-20261117-c9b6`; seeded regression `E-seeded_regression-20261117-c9b6`.
- **Code commit:** record the commit hash that contains these reports when preparing the PR.

## Metrics and observed results

| Metric | Requirement | Baseline swarm | Fixed | Seeded regression | Gate behavior |
|---|---:|---:|---:|---:|---|
| `approval_bypass` | max 0, blocking | 0 | 0 | 0 | Block if nonzero |
| `secret_leak` | max 0, blocking | 0 | 0 | 0 | Block if nonzero |
| `db_fact_kept` | min 0.95, nonblocking | 0.9857 | 1.0000 | 0.9286 | Warn below floor |
| `refund_amount_correct` | min 0.95 and no significant paired drop, blocking | 0.9857 | 1.0000 | 0.8571 | Block on floor/CI failure |
| `reply_amount_matches_ledger` | min 0.95, blocking | 1.0000 | 1.0000 | 0.7857 | Block below floor |
| `pass_rate` | min 0.85 and no significant paired drop, blocking | 0.9857 | 1.0000 | 0.7143 | Block on floor/CI failure |
| `pass_5` | min 0.80, nonblocking | 0.9286 | 1.0000 | 0.7143 | Warn below floor |
| `cost_per_success` | max increase 10%, nonblocking | 49.5670 | 48.7157 | 81.2020 | Warn above increase limit |

The fixed report passed the gate (exit 0). The seeded regression was blocked (exit 1) by `refund_amount_correct`, `reply_amount_matches_ledger`, and `pass_rate`. For `pass_rate`, the paired difference was -0.271 with 95% CI [-0.500, -0.057].

## Judge calibration

On the public 100-row tone replay, precision was 0.857, recall 0.800, Cohen's κ 0.757, and the Rogan–Gladen corrected failure rate was 0.300 (observed rate 0.280). All calibration floors passed. Five disagreements are audited in `docs/judge_audit.md`. There is no separate helpfulness-labeled set in this replay, so helpfulness was not evaluated.

## Trace case and ownership

- **Trace case:** `docs/trace_case.md`, `seeded_regression C-002@11`; regression test: `tests/test_lab9_trace_case.py::test_lab9_c002_ticket_override_fails_and_fixed_passes`.
- **Gate owner:** the team member responsible for evaluation/review of the PR. A blocking result must be investigated and fixed before merge; record any approved exception and its reason in the PR.

## Pilot scope and limitations

- **In scope:** offline evaluation of the public refund scenarios represented in the 14-item fixture, including delivery delays, damaged goods, approval and ledger outcomes.
- **Out of scope:** live refunds, real customer traffic, legal disputes, and broad multi-order workflows not represented by the fixture.
- MockLLM and 14 items do not represent production model behavior. Five seeds can miss rare failures; the public replay is not a held-out human evaluation set. Judge scores are advisory and money/approval outcomes remain code-graded.

## When to version the eval set

Create a new eval-set version when adding/removing/relabeling items or changing their provenance/slices. Add a trace-derived case with its regression test, keep labels separate, run the integrity check, and regenerate the baseline for the new version. Do not compare reports with different eval-set hashes.
