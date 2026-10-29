
from types import SimpleNamespace

import pygame
import pytest

from state.events import (
    invocation_policy,
    Callbacks,
    StateEventContext,
    EventsDict,
)


def test_iterable_invoke_all_returns_results_in_registration_order():
    callbacks = Callbacks()
    calls = []

    def first(ctx):
        calls.append("first")
        return 10

    def second(ctx):
        calls.append("second")
        return 20

    ctx = StateEventContext(
        active_state=SimpleNamespace(),  # type: ignore
        triggered_event=callbacks,
        dt=1 / 60,
    )

    callbacks.register(first)
    callbacks.register(second)

    results = callbacks._iterable_invoke_all(ctx)
    expected_results = [10, 20]

    for call_info, result in results:
        assert result == expected_results.pop(0)
    assert calls == ["first", "second"]


def test_invoke_all_on_empty_callbacks_returns_none():
    callbacks = Callbacks()
    ctx = StateEventContext(
        active_state=SimpleNamespace(),  # type: ignore
        triggered_event=callbacks,
    )

    assert callbacks._invoke_all(ctx) is None


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
        invocation_policy=invocation_policy.ONCE_PER_LOOP,
    )

    entries = dict(registry)

    keydown_registration = entries[pygame.KEYDOWN].registered_actions[0]
    keyup_registration = entries[pygame.KEYUP].registered_actions[0]

    assert keydown_registration.action is keyup_registration.action
    assert keydown_registration.action is callback


def test_same_function_can_be_registered_twice():
    registry = EventsDict()

    def callback(ctx):
        return None

    registry.register(pygame.KEYDOWN, callback)
    registry.register(pygame.KEYDOWN, callback)

    entries = dict(registry)[pygame.KEYDOWN]

    assert len(entries) == 2
    first = second = None
    for idx, action_info in enumerate(entries):
        assert action_info.action is callback
        if idx == 0:
            first = action_info
        else:
            second = action_info
    assert first is not second


def test_registering_none_trigger_raises_type_error():
    registry = EventsDict()

    def key_pressed(ctx):
        ...

    with pytest.raises(TypeError, match="Expected a trigger or iterable of triggers, got: None"):
        registry.register(None, key_pressed)


def test_registering_none_callback_raises_type_error():
    registry = EventsDict()

    with pytest.raises(AssertionError, match="Action can not be None"):
        registry.register(pygame.KEYDOWN, None)  # type: ignore
