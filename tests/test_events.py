from types import SimpleNamespace

from system.state.events.events import (
    EventsList,
    State_EventContext,
)


def test_invoke_internal_returns_results_in_order():
    callbacks = EventsList()
    calls = []

    def first(ctx):
        calls.append("first")
        return 10

    def second(ctx):
        calls.append("second")
        return 20

    # A lightweight stand-in is enough for this isolated test.
    state = SimpleNamespace()

    ctx = State_EventContext(
        active_state=state,
        activated_event=callbacks,
        dt=1 / 60,
    )

    callbacks.register(first)
    callbacks.register(second)

    results = callbacks.invoke_internal(ctx)

    assert calls == ["first", "second"]
    assert results == [10, 20]