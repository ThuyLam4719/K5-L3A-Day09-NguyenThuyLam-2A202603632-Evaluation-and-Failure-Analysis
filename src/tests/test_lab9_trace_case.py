"""Regression test for the C-002 ticket-vs-DB trace case documented in docs/trace_case.md."""

import pytest

pytestmark = pytest.mark.student


def test_lab9_c002_ticket_override_fails_and_fixed_passes():
    from lab9.trace_case import investigate

    broken = investigate("seeded_regression", "C-002", 11)["trial"]
    fixed = investigate("fixed", "C-002", 11)["trial"]

    overrides = [
        (index, event)
        for index, event in enumerate(broken["events"], start=1)
        if event.get("kind") == "model_override"
    ]
    assert overrides
    assert overrides[0][0] == 3
    assert overrides[0][1].get("payload", {}).get("delay_days") == 5
    assert broken["lab8_pass"] is False
    assert broken["snapshot"]["refund_vnd"] == 20000

    assert fixed["lab8_pass"] is True
    assert fixed["snapshot"]["refund_vnd"] == 0
