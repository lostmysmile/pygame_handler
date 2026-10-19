from __future__ import annotations

from collections import defaultdict, namedtuple
from typing import TYPE_CHECKING, Any, Callable, Generator, Iterable, LiteralString, Optional, Self, Union, Unpack
import pygame

from helper import debugger

if TYPE_CHECKING:
    from .. import State


from ..events import ENUMS


class Events_Iterable_Type:
    __slots__ = ()


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


class State_EventContext[EventType:Events_Iterable_Type | pygame.key.ScancodeWrapper | pygame.event.Event]:
    __slots__ = ("activated_event", "active_state", "dt")

    def __init__(self, active_state: State, activated_event: EventType, dt: Optional[int | float] = None) -> None:
        self.active_state: State = active_state
        self.activated_event: EventType = activated_event
        self.dt: int | float | None = dt

    def update(self, dt=None, active_state=None):
        if active_state is not None:
            self.active_state = active_state
        if dt is not None:
            self.dt = dt


class EventsList[R](Events_Iterable_Type):
    __slots__ = ("actions",)

    def __init__(self) -> None:
        self.actions: list[Callable[[State_EventContext[Self]], R]] = []

    def invoke_internal(self, ctx: State_EventContext[Self]) -> list[R]:
        return [action(ctx) for action in self.actions]

    def register(self, action: Callable[[State_EventContext[Self]], R]):
        self.actions.append((action))

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


class functions_list[TriggerType:int | ENUMS.ALL_TRIGGERS.TYPE | ENUMS.NO_TRIGGERS.TYPE | None,
                     EventContextType:Events_Iterable_Type | pygame.key.ScancodeWrapper | pygame.event.Event,
                     R= Any]:
    __slots__ = "iterable",

    def __init__(self) -> None:
        self.iterable: defaultdict[TriggerType,
                            list[CallableInfo[[State_EventContext[EventContextType]], R]]
                            ] = defaultdict(list)

    def _register_internal(self,
                           trigger: TriggerType,
                           func_info: CallableInfo[[State_EventContext[EventContextType]], R]):
        if func_info.action is None:
            raise ValueError("Cannot register NoneType")
        self.iterable[trigger].append(func_info)

    def register(
        self,
        triggers: Optional[
            TriggerType |
            Iterable[TriggerType]
        ] = ENUMS.NO_TRIGGERS.VALUE,
        func: Optional[Callable[[State_EventContext[EventContextType]], R]] = None,
        handle_once: bool = True,
        *,
        func_info: Optional[CallableInfo[[
            State_EventContext[EventContextType]], R]] = None
    ):
        new_func = func_info or CallableInfo(func, handle_once)  # type: ignore
    
        if (isinstance((triggers), str )):
            self._register_internal(triggers, new_func)

        elif isinstance(triggers, int):
            self._register_internal(triggers, new_func)

        elif isinstance(triggers, Iterable):
            for trigger in triggers:
                self._register_internal(trigger, new_func)

        else:
            raise TypeError(f"Unknown trigger type: {triggers} of type {type(triggers)}")


        if debugger.FLAGS.debug and debugger.FLAGS.event_registers:
            print(f"Registered {new_func!s} with trigger: {triggers!r}")
        return func

    def decorator_register(self,
                           triggers: Optional[
                               TriggerType |
                               Iterable[TriggerType]
                           ] = ENUMS.NO_TRIGGERS.VALUE,
                           func: Optional[Callable[[
                               State_EventContext[EventContextType]], R]] = None,
                           handle_once: bool = True,
                           *,
                           func_info: Optional[CallableInfo[[State_EventContext[EventContextType]], R]] = None):
        def wrapper(
            func: Callable[[State_EventContext[EventContextType]], R]
        ):

            self.register(triggers=triggers, func=func,
                          handle_once=handle_once, func_info=func_info)
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


class KeyboardEventsQueue(Events_Iterable_Type):
    __slots__ = ("actions",)

    def __init__(self) -> None:
        self.actions: functions_list[
            int | ENUMS.ALL_TRIGGERS.TYPE | ENUMS.NO_TRIGGERS.TYPE,
            pygame.event.Event,
            Any,
        ] = functions_list()


class MultiEventsLists(EventsList):
    __slots__ = ()


class FrameEventsQueue(MultiEventsLists):
    __slots__ = "before", "after"

    def __init__(self) -> None:
        self.before = EventsList[Self]()
        self.after = EventsList[Self]()


class StateEventsQueue(MultiEventsLists):
    __slots__ = "Draw_Events_Queue", "Update_Events_Queue"

    def __init__(self) -> None:
        self.Draw_Events_Queue = FrameEventsQueue()
        self.Update_Events_Queue = FrameEventsQueue()


class EventsHandler:
    def __init__(self) -> None:
        self.State_Events = StateEventsQueue()

        self.Keyboard_Event = KeyboardEventsQueue()
        self.Pygame_Event = KeyboardEventsQueue()
