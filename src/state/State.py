from __future__ import annotations

from itertools import chain
from typing import Any, Self, TYPE_CHECKING
from pygame.key import ScancodeWrapper
from collections import defaultdict, deque
from typing import Optional

from state.events import DrawEventContext, EventsHandler, StateEventContext

from .events import ENUMS as EVENT_NUMS


if TYPE_CHECKING:
    from ..system.main import Game

from helper import debug

import pygame

from pathlib import Path


from sys import path as sys_path
from .events import events
from graphics import EntitiesHandler


class NoMoreStates(Exception):
    ...


class NoPreviousStates(Exception):
    ...


def name_counter(name: str, names=defaultdict[str, int](int)):
    return names[name]


class State:
    _counter = -1

    def __new__(cls, handler: "States", name: str = "<GenericState:{}>") -> Self:
        State._counter += 1
        new_instance = super().__new__(cls)
        new_instance.name = name.format(name_counter(name))
        return new_instance

    def __init__(self, handler: "States", name: str) -> None:
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
        States.Global_Events.Keyboard_Event.pressed._invoke_all(ctx)
        self.events_handler.Keyboard_Event.pressed._invoke_all(ctx)

        ctx.triggered_event = keys_stream
        States.Global_Events.Keyboard_Event.pressed._invoke_all(ctx)
        self.events_handler.Keyboard_Event.pressed._invoke_all(ctx)


    def handle_pygame_events(self, pygame_events: list[pygame.event.Event]) -> None:
        handled = set()  # TODO find better name

        actions = (States.Global_Events.Pygame_Event.registered_actions |
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
                action_info.action(ctx)

    # def handle_pygame_events(self, pygame_events: list[pygame.event.Event]) -> None:

    #     events_with_type = {event.type: event for event in pygame_events}

    #     events_and_listeners = chain(
    #         States.Global_Events.Pygame_Event,
    #         self.events_handler.Pygame_Event
    #     )

    #     # if debug.FLAGS.debug_mode and debug.FLAGS.detailed_info:
    #     #     print((events_and_listeners))

    #     handled = set()

    #     for event_trigger, listeners in events_and_listeners:
    #         if event_trigger == EVENT_NUMS.TRIGGERS.NONE:
    #             if debug.FLAGS.debug_mode and debug.FLAGS.event_info:
    #                 print(f"<{event_trigger!r}<no-trigger> for {listeners!r}")

    #             continue

    #         if debug.FLAGS.debug_mode and debug.FLAGS.event_info and debug.FLAGS.detailed_info:
    #             if event_trigger != EVENT_NUMS.TRIGGERS.ALL:
    #                 print(f"Checking: {event_trigger!r}, {listeners!r}")

    #         event = events_with_type.get(event_trigger)  # type: ignore

    #         if (event_trigger == EVENT_NUMS.TRIGGERS.ALL) or (event is not None):
    #             for listener in listeners:
    #                 if listener.invocation_policy == EVENT_NUMS.invocation_policy.ONCE_PER_LOOP and listener.action in handled:
    #                     if debug.FLAGS.debug_mode and debug.FLAGS.event_info:
    #                         print(
    #                             f"Skipped {listener.action!r}; Has already been triggered")
    #                     continue

    #                 if debug.FLAGS.debug_mode and debug.FLAGS.event_info:
    #                     if event_trigger == EVENT_NUMS.TRIGGERS.ALL:
    #                         print(
    #                             f"handling <GENERIC_TRIGGER>{EVENT_NUMS.TRIGGERS.ALL} with", end="",
    #                         )
    #                     else:
    #                         assert isinstance(event_trigger, int)
    #                         print(
    #                             f"handling {event!r}"
    #                             f"({event_trigger}) with",
    #                             end="",
    #                         )

    #                     print(f"{listener}.")

    #                 if debug.FLAGS.debug_mode and debug.FLAGS.event_info:
    #                     print(
    #                         f"Triggering {listener.invocation_policy}: {listener.action!r} ")

    #                 ctx = StateEventContext(
    #                     self, event, dt=self.handler.game_handler.window.clock.dt)

    #                 listener.action(ctx)
    #                 if listener.invocation_policy == EVENT_NUMS.invocation_policy.ONCE_PER_LOOP:
    #                     handled.add(listener.action)

    def update(self, dt: float) -> None:
        ctx = StateEventContext(
            self, None, dt=dt)

        if debug.FLAGS.debug_mode:
            if debug.FLAGS.state_context_info:
                print("context:", ctx)

        self.handler.Global_Events.State_Events.update_events_Queue.before._invoke_all(
            ctx)
        self.events_handler.State_Events.update_events_Queue.before._invoke_all(ctx)

        self.entities.update()

        self.handler.Global_Events.State_Events.update_events_Queue.after._invoke_all(
            ctx)
        self.events_handler.State_Events.update_events_Queue.after._invoke_all(ctx)

    def draw_on(self, surf: pygame.Surface) -> None:
        ctx = DrawEventContext(self)

        if debug.FLAGS.debug_mode and debug.FLAGS.state_context_info:
            print("context:", ctx)

        self.handler.Global_Events.State_Events.draw_events_Queue.before._invoke_all(
            ctx)
        self.events_handler.State_Events.draw_events_Queue.before._invoke_all(ctx)

        self.entities.draw_on(surf)

        self.handler.Global_Events.State_Events.draw_events_Queue.after._invoke_all(
            ctx)
        self.events_handler.State_Events.draw_events_Queue.after._invoke_all(ctx)

    def on_leave(self):
        ctx = StateEventContext[None](self)
        if debug.FLAGS.states_transitions:
            print("Leaving", self, "...")
        States.Global_Events.State_Events.on_leave._invoke_all(ctx)
        self.events_handler.State_Events.on_leave._invoke_all(ctx)

    def on_enter(self):
        ctx = StateEventContext[None](self)
        if debug.FLAGS.states_transitions:
            print("Entering", self, "...")
        States.Global_Events.State_Events.on_enter._invoke_all(ctx)
        self.events_handler.State_Events.on_enter._invoke_all(ctx)


class States:
    Global_Events = EventsHandler()

    def __init__(self) -> None:
        self.prev_state: Optional[State] = None
        self.active_state: State

        self.deque: deque[State] = deque()

        self.default_state = State(self, "Default State")

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

        if debug.FLAGS.debug_mode and debug.FLAGS.states_transitions:
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

        if debug.FLAGS.debug_mode and debug.FLAGS.states_transitions:
            print(f"Switching state from: {self.prev_state} to {self.active_state}")


@States.Global_Events.Pygame_Event.decorator_register(pygame.QUIT)
def QUIT(ctx: StateEventContext):
    ctx.active_state.running = False
    print("Quitting...")
    return debug.show_message("Quitting...")


if __name__ == '__main__':
    states = States()

    def test_push_pop():
        state = State(states, "custom name")
        print(state.name)
    test_push_pop()
