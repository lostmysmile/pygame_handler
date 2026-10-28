from __future__ import annotations

from collections import defaultdict, namedtuple
from typing import TYPE_CHECKING, Any, Callable, Generator, Iterable, LiteralString, Optional, Self, Union, Unpack
import pygame

from helper import debugger

if TYPE_CHECKING:
    from .. import State


from ..events import ENUMS

type Trigger = int | ENUMS.TRIGGERS


class EventContext:
    __slots__ = ()


class StateEventContext[EventT](EventContext):
    __slots__ = ("triggered_event", "active_state", "dt")

    def __init__(
        self,
        active_state: State,
        triggered_event: EventT | None = None,
        dt: float | None = None,
    ) -> None:
        self.active_state = active_state
        self.triggered_event: EventT | None = triggered_event
        self.dt = dt

    def __str__(self) -> str:
        return (
            f"<StateEventContext["
            f"state={self.active_state}, "
            f"event={self.triggered_event!r}, "
            f"dt={self.dt}]>"
        )


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

    def _invoke_all_with_info(self, ctx: ContextT) -> list[tuple[CallbackInfo[[ContextT], R], R]]:
        return [
            (info, info.action(ctx))
            for info in self.registered_actions
        ]

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
    TriggerT:int | ENUMS.TRIGGERS,
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

        if not (
            type(trigger) is int
            or isinstance(trigger, ENUMS.TRIGGERS)
        ):
            raise TypeError(f"Unknown trigger type: {trigger!r}")

        if not callable(func):
            raise TypeError(f"Expected callable for func, got: {func!r}")

        self.registered_actions[trigger].register(
            func,
            invocation_policy=invocation_policy,
        )
        return func

    @property
    def registered_triggers(self):
        yield from self.registered_actions.keys()

    @property
    def registered_events(self):
        yield from self.registered_actions.values()

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
        self.update_events_Queue = EventsQueue[StateEventContext[None]](
        )
        self.on_enter = Callbacks[StateEventContext[None], Any]()
        self.on_leave = Callbacks[StateEventContext[None], Any]()


class EventsHandler:
    def __init__(self) -> None:
        self.State_Events = StateEvents()
        self.Keyboard_Event = EventsDict[int | ENUMS.TRIGGERS, pygame.event.Event]()
        self.Pygame_Event = EventsDict[int | ENUMS.TRIGGERS, pygame.event.Event]()
