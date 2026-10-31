from __future__ import annotations

from itertools import chain
from typing import Any, Self, TYPE_CHECKING
from pygame.key import ScancodeWrapper
from collections import defaultdict, deque

from pygame_handler.scene.events import DrawEventContext, EventsHandler, StateEventContext

from .events import ENUMS as EVENT_NUMS


if TYPE_CHECKING:
    from ..system.core import Game

from pygame_handler.helper.debugger import FLAGS
from pygame_handler.helper.logger import show_message

import pygame

from pathlib import Path


from sys import path as sys_path
from .events import events
from pygame_handler.graphics import EntitiesHandler


class NoMoreStates(Exception):
    ...


class NoPreviousStates(Exception):
    ...


def name_counter(name: str, names=defaultdict[str, int](int)):
    return names[name]

from operator import attrgetter

class Scene:
    _counter = -1

    def __new__(cls, handler: "Scenes_handler", name: str = "<GenericState:{}>") -> Self:
        Scene._counter += 1
        new_instance = super().__new__(cls)
        new_instance.name = name.format(name_counter(name))
        return new_instance

    def __init__(self, handler: "Scenes_handler", name: str) -> None:
        self.name: str
        self.running = True
        self.handler = handler
        self.entities = EntitiesHandler()
        self.events_handler = EventsHandler()

    def __str__(self):
        return f"<State[{self.name!r}]>"

    def __repr__(self) -> str:
        return f"<State[{self.name!r}] at 0x{id(self):016x}>"

    def handle_keyboard_input(self, keys_pressed: ScancodeWrapper,keys_stream:ScancodeWrapper) -> None:
        ctx = StateEventContext(self, keys_pressed)
        self._trigger_event(ctx,"Keyboard_Event","pressed")
        # Scenes_handler.Global_Events.Keyboard_Event.pressed._invoke_all(ctx)
        self.events_handler.Keyboard_Event.pressed._invoke_all(ctx)

        ctx.triggered_event = keys_stream
        self._trigger_event(ctx,"Keyboard_Event","streamed")
        # Scenes_handler.Global_Events.Keyboard_Event.streamed._invoke_all(ctx)
        # self.events_handler.Keyboard_Event.streamed._invoke_all(ctx)


    def handle_pygame_events(self, pygame_events: list[pygame.event.Event]) -> None:
        handled = set()  # TODO find better name

        actions = (Scenes_handler.Global_Events.Pygame_Event.registered_actions |
                   self.events_handler.Pygame_Event.registered_actions)

        for event in pygame_events:
            generic_actions = actions.get(EVENT_NUMS.TRIGGERS.ALL)

            specified_actions = actions.get(event.type)

            if not (generic_actions or specified_actions):
                continue

            triggered_actions = generic_actions | specified_actions  # type: ignore

            if not actions:
                continue

            ctx = StateEventContext(self, event)

            for action_info in triggered_actions:
                match action_info.invocation_policy:
                    case EVENT_NUMS.invocation_policy.ONCE_PER_LOOP:
                        if action_info in handled:
                            continue
                        else:
                            handled.add(action_info)
                # TODO hook state actions system
                # state_actions.handle(result)
                #? they can do custom actions triggered from `scene events` like:  (skip all remaining events, events, exit immediately, activate next scene after current frame,etc,) 
                action_info.action(ctx)

    def update(self, dt: float) -> None:
        ctx = StateEventContext(
            self, None, dt=dt)

        if FLAGS.debug_mode and FLAGS.state_context_info:
                print("context:", ctx)

        # self.handler.Global_Events.State_Events.update_events_Queue.before._invoke_all(
        #     ctx)
        # self.events_handler.State_Events.update_events_Queue.before._invoke_all(ctx)
        self._trigger_event(ctx,"State_Events","update_events_Queue.before")

        self.entities.update()

        self._trigger_event(ctx,"State_Events","update_events_Queue.after")
        # self.handler.Global_Events.State_Events.update_events_Queue.after._invoke_all(
        #     ctx)
        # self.events_handler.State_Events.update_events_Queue.after._invoke_all(ctx)

    def draw_on(self, surf: pygame.Surface) -> None:
        ctx = DrawEventContext(self)

        if FLAGS.debug_mode and FLAGS.state_context_info:
            print("context:", ctx)

        # self.handler.Global_Events.State_Events.draw_events_Queue.before._invoke_all(
        #     ctx)
        # self.events_handler.State_Events.draw_events_Queue.before._invoke_all(ctx)

        self._trigger_event(ctx,"State_Events","draw_events_Queue.before")

        self.entities.draw_on(surf)

        self._trigger_event(ctx,"State_Events","draw_events_Queue.after")
        # self.handler.Global_Events.State_Events.draw_events_Queue.after._invoke_all(
        #     ctx)
        # self.events_handler.State_Events.draw_events_Queue.after._invoke_all(ctx)

    def on_leave(self):
        if FLAGS.debug_mode and FLAGS.states_transitions:
            print(f"Leaving: {self}")

        ctx = StateEventContext[None](self)
        # Scenes_handler.Global_Events.State_Events.on_leave._invoke_all(ctx)
        # self.events_handler.State_Events.on_leave._invoke_all(ctx)
        
        self._trigger_event(ctx,"State_Events","on_leave")

    def on_enter(self):
        if FLAGS.debug_mode and FLAGS.states_transitions:
            print(f"Entering: {self}")

        ctx = StateEventContext[None](self)
        # Scenes_handler.Global_Events.State_Events.on_enter._invoke_all(ctx)
        # self.events_handler.State_Events.on_enter._invoke_all(ctx)

        self._trigger_event(ctx,"State_Events","on_enter")
        
    def _trigger_event(self,ctx: StateEventContext|DrawEventContext,event_type:str,event_name:str):
        invoker_name = "_invoke_all"
        
        global_events_getter = attrgetter(f"{event_type}.{event_name}.{invoker_name}")
        local_events_getter=attrgetter(f"{event_type}.{event_name}.{invoker_name}")

        global_events_invoker = global_events_getter(Scenes_handler.Global_Events)
        local_events_invoker = local_events_getter(self.events_handler)
        
        global_events_invoker(ctx)
        local_events_invoker(ctx)


class Scenes_handler:
    Global_Events = EventsHandler()

    def __init__(self) -> None:
        self.prev_state: Scene|None = None
        self.active_state: Scene

        self.deque: deque[Scene] = deque()

        self.default_state = Scene(self, "Default State")

    def __bool__(self):
        return bool(self.deque)

    def __iter__(self):
        yield from self.deque

    def with_handler(self, handler: Game):
        self.game_handler = handler
        return self

    def activate_previous_state(self):
        if self.prev_state is None:
            raise NoPreviousStates("Can not rollback on first state")

        if FLAGS.debug_mode and FLAGS.states_transitions:
            print(f"Switching state from: {self.active_state} to {self.prev_state}")

        self.active_state.on_leave()
        self.prev_state.on_enter()
        self.active_state = self.prev_state

        self.deque.appendleft(self.prev_state)
        self.prev_state = None

    def activate_next_state(self):
        try:
            self.prev_state = self.active_state
        except AttributeError:
            ...
        else:
            self.prev_state.on_leave()

        try:
            self.active_state = self.deque.pop()
        except IndexError:
            raise NoMoreStates("No states left in queue") from None
        else:
            self.active_state.on_enter()

        if FLAGS.debug_mode and FLAGS.states_transitions:
            print(f"Switching state from: {self.prev_state} to {self.active_state}")


@Scenes_handler.Global_Events.Pygame_Event.decorator_register(pygame.QUIT)
def QUIT(ctx: StateEventContext):
    ctx.active_state.running = False
    print("Quitting...")
    return show_message("Quitting...")


if __name__ == '__main__':
    states = Scenes_handler()

    def test_push_pop():
        state = Scene(states, "custom name")
        print(state.name)
    test_push_pop()
