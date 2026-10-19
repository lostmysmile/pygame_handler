from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    if __package__:
        from ..state import State
    else:
        from state import State

import pygame
from enum import StrEnum
from itertools import chain
from typing import Any, Callable, Literal


class ENUMS(StrEnum):
    ANY_TRIGGER = "{ANY}"


class registered_func[TriggerType, **P, R]:
    __slots__ = "trigger", "action", "handle_once"

    def __init__(
        self,
        trigger: TriggerType,
        action: Callable[P, R],
        handle_once: bool = True,
    ):
        self.trigger: TriggerType = trigger
        self.action: Callable[P, R] = action
        self.handle_once: bool = handle_once

    def __iter__(self):
        yield self.trigger
        yield self.action
        yield self.handle_once


class State_EventContext[EventType]:

    __slots__ = ("activated_event", "active_state", "dt")

    dt: int
    active_state: State
    activated_event: EventType

    def update(self, dt=None, active_state=None):
        if active_state is not None:
            self.active_state = active_state
        if dt is not None:
            self.dt = dt


class Registered_Actions[TriggerType, EventContextType, R = Any]:
    iterable: list[
        registered_func[
            TriggerType,
            [State_EventContext[EventContextType]],
            R
        ]
    ] = []

    def decorator_register(self, trigger: TriggerType, handle_once: bool = True):
        def wrapper(
            func: Callable[[State_EventContext[EventContextType]], R]
        ):
            new_func = registered_func(trigger, func, handle_once)
            self.iterable.append(new_func)
            return func

        return wrapper

    def register(
        self,
        trigger: TriggerType,
        func: Callable[[State_EventContext[EventContextType]], R],
        handle_once: bool = True,
    ):
        new_func = registered_func(trigger, func, handle_once)
        self.iterable.append(new_func)

    def __iter__(self):
        yield from self.iterable


class Event:
    __slots__ = "actions",

    context = State_EventContext["Event"]()

    def __init__(self) -> None:
        self.actions: list[Callable[[State_EventContext[Event]], Any]] = []

    def invoke_internal(self):
        self.context.activated_event = self
        for action in self.actions:
            action(self.context)

    def register(self, action: Callable[[State_EventContext[Event]], Any]):
        self.actions.append((action))


class QueuedEvent:
    __slots__ = "before_render", "after_render"

    def __init__(self) -> None:
        self.before_render = Event()
        self.after_render = Event()


class StateEvents:
    __slots__ = "Draw_Event", "Update_Event"

    def __init__(self) -> None:
        self.Draw_Event = QueuedEvent()
        self.Update_Event = QueuedEvent()


class KeyboardEvents:
    list: Registered_Actions[
        int | Literal[ENUMS.ANY_TRIGGER],
        KeyboardEvents,
        Any,
    ] = Registered_Actions()
    __slots__ = ()

    context = State_EventContext()

    def __init__(self) -> None:
        self.context.activated_event = self


class PygameEvents:
    Events_List: Registered_Actions[
        int | Literal[ENUMS.ANY_TRIGGER],
        PygameEvents,
        Any,
    ] = Registered_Actions()
    __slots__ = ()

    context: State_EventContext[PygameEvents] = State_EventContext["PygameEvents"]()


class EventsHandler:
    def __init__(self) -> None:
        self.State_Events = StateEvents()
        self.Keyboard_Event = KeyboardEvents()
        self.Pygame_Event = PygameEvents()
