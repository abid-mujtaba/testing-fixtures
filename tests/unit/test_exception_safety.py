"""
Tests for Fixture's exception-safety during entry.

`Fixture.__enter__` only resets `_entries` (and re-raises cleanly) when
`self._func(*args, **kwargs)` fails. If the fixture body itself raises anything
other than `StopIteration` on its first `next()` call (e.g. a genuine bug in the
fixture's setup code), `_entries` is left at 1 forever and `__exit__` never runs,
permanently corrupting the (module-level, shared) `Fixture` instance for every
later test that uses it.
"""

import pytest

from testing.fixtures import Fixture, FixtureDefinition, fixture

EXPECTED_CALL_COUNT_AFTER_RECOVERY = 2


class SetupError(Exception):
    """Raised by a fixture's setup code to simulate a real bug (not StopIteration)."""


def _make_flaky_fixture() -> tuple[Fixture[str, []], dict[str, int]]:
    """Create a fixture whose generator raises SetupError on its first call only."""
    calls = {"count": 0}
    setup_error_message = "boom"

    @fixture
    def flaky() -> FixtureDefinition[str]:
        calls["count"] += 1
        if calls["count"] == 1:
            raise SetupError(setup_error_message)
        yield "value"

    return flaky, calls


def test_failed_setup_resets_entries() -> None:
    """After setup raises (not StopIteration), the Fixture must reset to unentered."""
    flaky, _ = _make_flaky_fixture()

    with pytest.raises(SetupError), flaky:
        pass

    assert flaky._entries == 0


def test_fixture_usable_after_failed_setup() -> None:
    """A Fixture must be usable again (fresh setup) after a prior setup failure."""
    flaky, calls = _make_flaky_fixture()

    with pytest.raises(SetupError), flaky:
        pass

    # A later, independent use of the same (shared) Fixture instance must re-run
    # setup rather than silently reusing stale/absent state from the failed entry.
    with flaky as value:
        assert value == "value"

    assert calls["count"] == EXPECTED_CALL_COUNT_AFTER_RECOVERY
