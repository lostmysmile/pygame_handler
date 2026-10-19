from __future__ import annotations

from collections import namedtuple
from typing import TYPE_CHECKING, Any, Callable, Unpack

if TYPE_CHECKING:
    if __package__:
        from .. import State
    else:
        from state import State


from ..events import ENUMS


class registered_func[**P, R]:
    __slots__ = "action", "handle_once"

    def __init__(self,
                 action: Callable[P, R],
                 handle_once: bool = True,
                 ):

        self.action: Callable[P, R] = action
        self.handle_once: bool = handle_once

    def __iter__(self):
        yield self.action
        yield self.handle_once


class State_EventContext[EventType]:
    __slots__ = ("activated_event", "active_state", "dt")

    def __init__(self) -> None:
        self.dt: int
        self.active_state: State
        self.activated_event: EventType

    def update(self, dt=None, active_state=None):
        if active_state is not None:
            self.active_state = active_state
        if dt is not None:
            self.dt = dt


class Registered_Actions[TriggerType, EventContextType, R = Any]:
    __slots__ = "iterable",

    def __init__(self) -> None:
        self.iterable: dict[TriggerType | ENUMS.TYPE_ANY_TRIGGER | None,
                            list[registered_func[[State_EventContext[EventContextType]], R]]
                            ] = {ENUMS.ANY_TRIGGER: list()}

    def register(
        self,
        trigger: TriggerType | ENUMS.TYPE_ANY_TRIGGER |None ,
        func: Callable[[State_EventContext[EventContextType]], R],
        handle_once: bool = True,
    ):

        self.iterable.setdefault(trigger, list()).append(registered_func(func, handle_once))

    def decorator_register(self,
                           trigger: TriggerType | ENUMS.TYPE_ANY_TRIGGER | None = None,
                           handle_once: bool = True):
        def wrapper(
            func: Callable[[State_EventContext[EventContextType]], R]
        ):
            self.register(trigger=trigger, func=func, handle_once=handle_once)
            return func

        return wrapper

    @property
    def registered_triggers(self):
        yield from self.iterable.keys()

    @property
    def registered_events(self):
        yield from self.iterable.values()

    def __iter__(self):
        yield from self.iterable.items()


class Event:
    __slots__ = "actions", "context"

    def __init__(self) -> None:
        self.context = State_EventContext["Event"]()
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
        int | ENUMS.TYPE_ANY_TRIGGER,
        KeyboardEvents,
        Any,
    ] = Registered_Actions()
    __slots__ = ()

    context = State_EventContext()

    def __init__(self) -> None:
        self.context.activated_event = self


class PygameEvents:
    __slots__ = ()

    context: State_EventContext[PygameEvents] = State_EventContext["PygameEvents"]()

    Events_List: Registered_Actions[
        int,
        PygameEvents,
        Any,
    ] = Registered_Actions()


class EventsHandler:
    def __init__(self) -> None:
        self.State_Events = StateEvents()
        self.Keyboard_Event = KeyboardEvents()
        self.Pygame_Event = PygameEvents()
