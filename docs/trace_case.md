# Trace case: ticket override causes an incorrect refund

## Trial

- **Trial:** `seeded_regression C-002@11`
- **Eval report:** `E-seeded_regression-20261117-c9b6` (eval-set SHA `c9b66b3c6276`).
- **Claim:** C-002 ticket says delivery was delayed 5 days; the order row in the DB says 2 days. The expected outcome is denied with no refund.
- **Observed result:** Lab 8 grader fails with `status resolved != denied`. The ledger contains 20,000 VND, while the expected amount is 0 VND.
- **Failure mode:** FM-03 `ticket_trust`.

## First wrong step

The first wrong event is **event 3, `model_override`**: `{"delay_days": 5}`. Event 1 creates the handoff and event 2 reads the order from the DB. Those events do not change the DB value. Event 3 replaces the DB delay of 2 days with the ticket's claim of 5 days. The following quote and refund are consequences of that override.

## Fixed-shape contrast

For the same `C-002@11` trial, shape `fixed` does not emit `model_override`. It quotes 0 VND, leaves the ledger at 0 VND, and the Lab 8 grader passes with `ok`.

Commands to reproduce both traces from `src/`:

```powershell
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11
```

## Regression test

`tests/test_lab9_trace_case.py::test_lab9_c002_ticket_override_fails_and_fixed_passes` reproduces the same claim and seed. It asserts that the seeded regression first overrides the DB fact at event 3 and fails the grader with a 20,000 VND refund, while `fixed` passes and leaves the ledger at 0 VND. `DbFactKept` also flags the `model_override` event.

## Limits

This is one public fixture and one seed. It demonstrates the failure mechanism for this case; it does not estimate its frequency on real traffic or prove coverage for every type of ticket/DB disagreement.
