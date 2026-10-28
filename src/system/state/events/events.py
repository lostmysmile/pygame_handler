from __future__ import annotations

from collections import defaultdict, namedtuple
from typing import TYPE_CHECKING, Any, Callable, Generator, Iterable, LiteralString, Optional, Self, Union, Unpack
import pygame

from helper import debugger

if TYPE_CHECKING:
    from .. import State


from ..events import ENUMS


class EventContext[EventType]:
    __slots__ = ("triggered_event", "active_state", "dt")

    def __init__(self, active_state: State, triggered_event: EventType, dt: Optional[int | float] = None) -> None:
        self.active_state: State = active_state
        self.triggered_event: EventType = triggered_event
        self.dt: int | float | None = dt

    def update(self, dt=None, active_state=None):
        if active_state is not None:
            self.active_state = active_state
        if dt is not None:
            self.dt = dt


class CallableInfo[**P, R]:
    __slots__ = "action", "handle_once"

    def __init__(self,
                 action: Callable[P, R],
                 handle_once: bool = True,
                 ):

        self.action: Callable[P, R] = action
        self.handle_once: bool = handle_once

    def __str__(self):
        return f"<{self.action} runs {"once" if self.handle_once else "multiple times"}>"

    def __iter__(self):
        yield self.action
        yield self.handle_once


class RegisteredFuncs[EventContextType, R]:
    __slots__ = ("registered_actions",)

    def __init__(self) -> None:
        self.registered_actions: list[CallableInfo[[
            EventContext[EventContextType]], R]] = []

    def __iter__(self):
        yield from self.registered_actions

    def _invoke_all(self, ctx: EventContext[EventContextType]) -> list[tuple[CallableInfo[[EventContext[EventContextType]], R], R]]:
        return [(action_info, action_info.action(ctx)) for action_info in self.registered_actions]

    def register(self, action: Callable[[EventContext[EventContextType]], R], handle_once=True):
        new_func = CallableInfo(action, handle_once=handle_once)
        self.registered_actions.append(new_func)
        return action


allowed_trigger_types = ()
(pygame.event.Event, pygame.key.ScancodeWrapper,
 ENUMS.ALL_TRIGGERS.TYPE, ENUMS.NO_TRIGGERS.TYPE)


class EventsList[TriggerType,
                 EventContextType,
                 R = Any]:

    __slots__ = "registered_actions",

    def __init__(self) -> None:
        self.registered_actions: defaultdict[TriggerType,
                                             RegisteredFuncs
                                             ] = defaultdict(RegisteredFuncs)

    def _register_internal(self,
                           trigger: TriggerType,
                           func: Callable[[EventContext[EventContextType]], R],
                           handle_once=True):
        if (type(trigger)) not in allowed_trigger_types:
            raise TypeError(f"unknown trigger type: {type(trigger)}")
        self.registered_actions[trigger].register(func, handle_once=handle_once)
        return func

    def register(
        self,
        triggers: Optional[
            TriggerType |
            Iterable[TriggerType]
        ],
        func: Callable[[EventContext[EventContextType]], R],
        handle_once: bool = True,

    ):
        if not callable(func):
            raise TypeError(f"Expected callable for func got: {func}")

        if (isinstance((triggers), (str, pygame.key.ScancodeWrapper, pygame.event.Event))):
            result = (
                self._register_internal(triggers, func, handle_once=handle_once))

        elif isinstance(triggers, Iterable):
            result = [
                self._register_internal(trigger, func, handle_once=handle_once)
                for trigger in triggers]
        elif triggers is None:
            result = (
                self._register_internal(ENUMS.NO_TRIGGERS.VALUE,
                                        func, handle_once=handle_once))
        else:
            raise TypeError(f"Unknown trigger type: {triggers} of type {type(triggers)}")

        if debugger.FLAGS.debug and debugger.FLAGS.event_registers:
            print(f"Registered {func!s} with trigger: {triggers!r}")

        return result

    def decorator_register(self,
                           triggers: Optional[
                               TriggerType |
                               Iterable[TriggerType]
                           ] = ENUMS.NO_TRIGGERS.VALUE,
                           handle_once: bool = True,
                           ):
        def wrapper(
            func: Callable[[EventContext[EventContextType]], R]
        ):

            return self.register(triggers=triggers, func=func,
                                 handle_once=handle_once)

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
        self.before = RegisteredFuncs()
        self.after = RegisteredFuncs()


class StateEvents:
    __slots__ = "draw_events_Queue", "update_events_Queue"

    def __init__(self) -> None:
        self.draw_events_Queue = EventsQueue()
        self.update_events_Queue = EventsQueue()


class EventsHandler:
    def __init__(self) -> None:
        self.State_Events = StateEvents()
        self.Keyboard_Event = RegisteredFuncs()
        self.Pygame_Event = RegisteredFuncs()
