
from types import SimpleNamespace

import pygame
import pytest

from system.state.events.events import (
    Callbacks,
    StateEventContext,
    EventsDict,
)


def test_invoke_internal_returns_results_in_order():
    callbacks = Callbacks()
    calls = []

    def first(ctx):
        calls.append("first")
        return 10

    def second(ctx):
        calls.append("second")
        return 20

    ctx = StateEventContext(
        active_state=SimpleNamespace(),
        triggered_event=callbacks,
        dt=1 / 60,
    )

    callbacks.register(first)
    callbacks.register(second)

    results = callbacks._invoke_all(ctx)

    assert calls == ["first", "second"]
    assert results == [10, 20]


def test_empty_events_list_returns_empty_results():
    callbacks = Callbacks()
    ctx = StateEventContext(
        active_state=SimpleNamespace(),
        triggered_event=callbacks,
    )

    assert callbacks._invoke_all(ctx) == []


# def test_context_update_accepts_zero_dt():
#     original_state = SimpleNamespace(name="original")
#     new_state = SimpleNamespace(name="new")
#     ctx = EventContext(
#         active_state=original_state,
#         triggered_event=EventsList(),
#         dt=1 / 60,
#     )

#     ctx.update(dt=0, active_state=new_state)

#     assert ctx.active_state is new_state
#     assert ctx.dt == 0




def test_multiple_triggers_share_one_registration():
    registry = EventsDict()

    def callback(ctx):
        return None

    registry.register(
        [pygame.KEYDOWN, pygame.KEYUP],
        callback,
        invocation_policy=False,
    )

    entries = dict(registry)

    keydown_registration = entries[pygame.KEYDOWN][0]
    keyup_registration = entries[pygame.KEYUP][0]

    assert keydown_registration is keyup_registration
    assert keydown_registration.action is callback


def test_same_function_can_be_registered_twice():
    registry = EventsDict()

    def callback(ctx):
        return None

    registry.register(pygame.KEYDOWN, callback)
    registry.register(pygame.KEYDOWN, callback)

    entries = dict(registry)[pygame.KEYDOWN]

    assert len(entries) == 2
    assert entries[0].action is callback
    assert entries[1].action is callback
    assert entries[0] is not entries[1]


def test_registering_none_raises_value_error():
    registry = EventsDict()

    with pytest.raises(ValueError, match="Cannot register NoneType"):
        registry.register(pygame.KEYDOWN)
