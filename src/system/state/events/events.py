from __future__ import annotations

from collections import defaultdict, namedtuple
from typing import TYPE_CHECKING, Any, Callable, Generator, Iterable, LiteralString, Optional, Self, Union, Unpack
import pygame

from helper import debugger

if TYPE_CHECKING:
    from .. import State


from ..events import ENUMS


class EventContext:
    __slots__ = ()


class StateEventContext[EventType](EventContext):
    __slots__ = ("triggered_event", "active_state", "dt")

    def __init__(self, active_state: State, triggered_event: EventType, dt: Optional[int | float] = None) -> None:
        self.active_state: State = active_state
        self.triggered_event: EventType = triggered_event
        self.dt: int | float | None = dt

    def __str__(self) -> str:
        return f"<EventContext[state={self.active_state},event={self.triggered_event},dt={self.dt}]"

    def update(self, *, dt=None, active_state=None):
        if active_state is not None:
            self.active_state = active_state
        if dt is not None:
            self.dt = dt


class DrawEventContext(EventContext):
    __slots__ = ("active_state")

    def __init__(self, active_state: State) -> None:
        self.active_state: State = active_state

    def __str__(self) -> str:
        return f"<DrawEventContext[state={self.active_state}]"

    def update(self, active_state):
        self.active_state = active_state


class CallbackInfo[**P, R]:
    __slots__ = "action", "invocation_policy"

    def __init__(self,
                 action: Callable[P, R],
                 invocation_policy: ENUMS.invocation_policy = ENUMS.invocation_policy.ONCE_PER_LOOP,
                 ):

        self.action: Callable[P, R] = action
        self.invocation_policy: ENUMS.invocation_policy = invocation_policy

    def __str__(self):
        return f"<{self.action!r} policy={self.invocation_policy}>"

    def __iter__(self):
        yield self.action
        yield self.invocation_policy


class Callbacks[ContextT, R= Any]:
    __slots__ = ("registered_actions",)

    def __init__(self) -> None:
        self.registered_actions: list[
            CallbackInfo[[ContextT], R]
        ] = []

    def __iter__(self):
        yield from self.registered_actions

    def _invoke_all(self, ctx: ContextT) -> list[R]:
        return [
            info.action(ctx)
            for info in self.registered_actions
        ]

    def register(
        self,
        action: Callable[[ContextT], R],
        invocation_policy: ENUMS.invocation_policy
        = ENUMS.invocation_policy.ONCE_PER_LOOP,
    ) -> Callable[[ContextT], R]:
        info = CallbackInfo(
            action,
            invocation_policy=invocation_policy,
        )
        self.registered_actions.append(info)
        return action




class EventsDict[
    TriggerT,
    EventT,
    ReturnT = Any,
]:
    __slots__ = ("registered_actions",)

    def __init__(self) -> None:
        self.registered_actions: defaultdict[
            TriggerT,
            Callbacks[StateEventContext[EventT], ReturnT],
        ] = defaultdict(
            Callbacks[StateEventContext[EventT], ReturnT]
        )

    def _register_internal(
        self,
        trigger: TriggerT,
        func: Callable[[StateEventContext[EventT]], ReturnT],
        invocation_policy: ENUMS.invocation_policy
        = ENUMS.invocation_policy.ONCE_PER_LOOP,
    ) -> Callable[[StateEventContext[EventT]], ReturnT]:
        if not callable(func):
            raise TypeError(f"Expected callable for func, got: {func!r}")

        if type(trigger) is not int:
            raise TypeError(f"Unknown trigger type: {type(trigger)}")

        self.registered_actions[trigger].register(
            func,
            invocation_policy=invocation_policy,
        )
        return func



class OptionsEnabledList():
    """
    TODO make events (callables) that can be executed on each frame 
    (or variable frame) 
    ex: every 1 frame or 10 frames
    (with or without an option required) option: variable that simulates settings for the game engine
    ex: if Game.Options.Stepped_Frames=ON > every {variable; mentioned above} frame wait until keyboard.get_pressed("Enter") 
    ! not each pause should the engine fix movements from delta time or else things would teleport far ahead
        ? check elapsed time and subtract from the dt to get accurate measures
    """
    ...


class EventsQueue[ContextT, R = Any]:
    __slots__ = "before", "after"

    def __init__(self) -> None:
        self.before: Callbacks[ContextT, R] = Callbacks[ContextT, R]()
        self.after: Callbacks[ContextT, R] = Callbacks[ContextT, R]()


class StateEvents:
    __slots__ = "draw_events_Queue", "update_events_Queue", "on_enter", "on_leave"

    def __init__(self) -> None:
        self.draw_events_Queue = EventsQueue[DrawEventContext]()
        self.update_events_Queue = EventsQueue[StateEventContext[self.update_events_Queue]](
        )
        self.on_enter = Callbacks[StateEventContext[self.on_enter], Any]()
        self.on_leave = Callbacks[StateEventContext[self.on_leave], Any]()


class EventsHandler:
    def __init__(self) -> None:
        self.State_Events = StateEvents()
        self.Keyboard_Event = EventsDict[int, int]()
        self.Pygame_Event = EventsDict[int, int]()
