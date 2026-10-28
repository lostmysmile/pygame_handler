from __future__ import annotations

from collections import defaultdict, namedtuple
from typing import TYPE_CHECKING, Any, Callable, Generator, Iterable, LiteralString, Optional, Self, Union, Unpack
import pygame

from helper import debugger

if TYPE_CHECKING:
    from .. import State


from ..events import ENUMS


class EventContext:
    __slots__=()
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
        return f"<{self.action} runs {"once" if self.invocation_policy else "multiple times"}>"

    def __iter__(self):
        yield self.action
        yield self.invocation_policy


class Callbacks[EventContextType, R]:
    __slots__ = ("registered_actions",)

    def __init__(self) -> None:
        self.registered_actions: list[CallbackInfo[[
            StateEventContext[EventContextType]], R]] = []

    def __iter__(self):
        yield from self.registered_actions

    def _invoke_all(self, ctx: StateEventContext[EventContextType]) -> list[tuple[CallbackInfo[[StateEventContext[EventContextType]], R], R]]:
        return [(action_info, action_info.action(ctx)) for action_info in self.registered_actions]

    def register(self, action: Callable[[StateEventContext[EventContextType]], R], invocation_policy: ENUMS.invocation_policy = ENUMS.invocation_policy.ONCE_PER_LOOP):
        new_func = CallbackInfo(action, invocation_policy=invocation_policy)
        self.registered_actions.append(new_func)
        return action


allowed_trigger_types = (int,)


class EventsDict[TriggerType,
                 EventContextType,
                 R = Any]:

    __slots__ = "registered_actions",

    def __init__(self) -> None:
        self.registered_actions: defaultdict[
            TriggerType,
            Callbacks[EventContextType, R]] = defaultdict(Callbacks[EventContextType, R])

    def _register_internal(self,
                           trigger: TriggerType,
                           func: Callable[[StateEventContext[EventContextType]], R],
                           invocation_policy: ENUMS.invocation_policy = ENUMS.invocation_policy.ONCE_PER_LOOP):
        if (type(trigger)) not in allowed_trigger_types:
            raise TypeError(f"unknown trigger type: {type(trigger)}")
        self.registered_actions[trigger].register(
            func, invocation_policy=invocation_policy)
        return func

    def register(
        self,
        triggers: Optional[
            TriggerType | Iterable[TriggerType]
        ],
        func: Callable[[StateEventContext[EventContextType]], R],
        invocation_policy: ENUMS.invocation_policy = ENUMS.invocation_policy.ONCE_PER_LOOP,

    ):
        if not callable(func):
            raise TypeError(f"Expected callable for func got: {func}")

        if isinstance(triggers, Iterable):
            for trigger in triggers:
                self._register_internal(
                    trigger, func, invocation_policy=invocation_policy)
        elif (isinstance((triggers), (str, pygame.key.ScancodeWrapper, int))):
            (self._register_internal(triggers, func, invocation_policy=invocation_policy))

        elif triggers is None:
            (self._register_internal(ENUMS.NO_TRIGGERS.VALUE,
                                     func, invocation_policy=invocation_policy))
        else:
            raise TypeError(
                f"Unknown trigger type: {triggers}({type(triggers)}) for {func}")

        if debugger.FLAGS.debug and debugger.FLAGS.event_registers:
            print(f"Registered {func!s} with trigger: {triggers!r}")

        return func

    def decorator_register(self,
                           triggers: Optional[
                               TriggerType |
                               Iterable[TriggerType]
                           ] = ENUMS.NO_TRIGGERS.VALUE,
                           invocation_policy: ENUMS.invocation_policy = ENUMS.invocation_policy.ONCE_PER_LOOP,
                           ):
        def wrapper(
            func: Callable[[StateEventContext[EventContextType]], R]
        ):

            return self.register(triggers=triggers, func=func,
                                 invocation_policy=invocation_policy)

        return wrapper

    @property
    def registered_triggers(self):
        yield from self.registered_actions.keys()

    @property
    def registered_events(self):
        yield from self.registered_actions.values()

    def __iter__(self):
        yield from self.registered_actions.items()


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


class EventsQueue:
    __slots__ = "before", "after"

    def __init__(self) -> None:
        self.before = Callbacks()
        self.after = Callbacks()


class StateEvents:
    __slots__ = "draw_events_Queue", "update_events_Queue", "on_enter", "on_leave"

    def __init__(self) -> None:
        self.draw_events_Queue = EventsQueue()
        self.update_events_Queue = EventsQueue()
        self.on_enter = Callbacks()
        self.on_leave = Callbacks()


class EventsHandler:
    def __init__(self) -> None:
        self.State_Events = StateEvents()
        self.Keyboard_Event = EventsDict()
        self.Pygame_Event = EventsDict()
