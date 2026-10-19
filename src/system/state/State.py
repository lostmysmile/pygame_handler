
from itertools import chain
from typing import Self, TYPE_CHECKING
from pygame.key import ScancodeWrapper
from collections import deque
from typing import Optional


if TYPE_CHECKING:
    from ..main import Game

from helper import debugger

import pygame

from pathlib import Path


from sys import path as sys_path
from .events import EventsHandler, State_EventContext, events, ENUMS as EVENT_NUMS
from ..graphics import EntitiesHandler


class NoMoreStates(StopIteration):
    ...


class NoPreviousStates(StopIteration):
    ...


class State:
    _counter = 0

    def __new__(cls, handler: "States", name: str = "<GenericState:{}>") -> Self:
        new_instance = super().__new__(cls)
        new_instance.name = name.format(State._counter)
        return new_instance

    def __init__(self, handler: "States") -> None:
        self.name: str
        self.running = True
        self.handler = handler
        self.entities = EntitiesHandler()
        self.events_handler = EventsHandler()

    def handle_keyboard_input(self, keys: ScancodeWrapper) -> None:
        pygame.key.set_text_input_rect
        keys_stream = pygame.key.get_pressed()
        pressed_keys = pygame.key.get_just_pressed()
        # TODO implement
        # self.global_events.Keyboard_Event
        # self.local_events.Keyboard_Event
        # raise NotImplementedError()
        pass  # Default: do nothing

    def handle_pygame_events(self, pygame_events: list[pygame.Event]) -> None:
        handled = set()
        events_and_listeners = chain(
            States.Global_Events.Pygame_Event.actions,
            self.events_handler.Pygame_Event.actions)

        if debugger.FLAGS.debug and debugger.FLAGS.detailed_info:
            print(events_and_listeners)

        for event_trigger, listeners in events_and_listeners:
            if not listeners:
                continue

            if event_trigger == EVENT_NUMS.NO_TRIGGERS.VALUE:
                if debugger.FLAGS.debug and debugger.FLAGS.event_info:
                    print(f"<{event_trigger!r}<no-trigger> for {listeners!r}")

                continue

            if debugger.FLAGS.debug and debugger.FLAGS.event_info and debugger.FLAGS.detailed_info:
                if event_trigger != EVENT_NUMS.ALL_TRIGGERS:
                    print(f"Checking: {event_trigger!r}, {listeners!r}")

            if (event_trigger == EVENT_NUMS.ALL_TRIGGERS) or (event_trigger in pygame_events):
                for listener in listeners:
                    if listener.handle_once is True and listener.action in handled:
                        if debugger.FLAGS.debug and debugger.FLAGS.event_info:
                            print(
                                f"Skipped {listener.action!r}; Has already been triggered")
                        continue

                    if debugger.FLAGS.debug and debugger.FLAGS.event_info:
                        if event_trigger == EVENT_NUMS.ALL_TRIGGERS:
                            print(
                                f"handling <GENERIC_TRIGGER>{EVENT_NUMS.ALL_TRIGGERS!r} with", end="",
                            )
                        else:
                            assert isinstance(event_trigger, int)
                            print(
                                f"handling {pygame.event.event_name(event_trigger)!r}"
                                f"({event_trigger}) with",
                                end="",
                            )

                        print(f"{listener}.")

                    if debugger.FLAGS.debug and debugger.FLAGS.event_info:
                        print(
                            f"Triggering: {listener.action!r} <HANDLE_ONCE={listener.handle_once!r}>")

                    if isinstance(event_trigger,str ):
                        ctx = State_EventContext(
                        self, EVENT_NUMS.ALL_TRIGGERS.VALUE)
                    else:
                        ctx = State_EventContext(
                        self, pygame_events[pygame_events.index(event_trigger)])

                    listener.action(ctx)
                    if listener.handle_once:
                        handled.add(listener.action)

    def update(self, dt: float) -> None:
        ctx = State_EventContext(
            self, self.events_handler.State_Events.Update_Events_Queue)

        if debugger.FLAGS.debug:
            if debugger.FLAGS.state_context_info:
                print("context:", ctx)
        self.handler.Global_Events.State_Events.Update_Events_Queue.before.invoke_internal(
            ctx)
        self.events_handler.State_Events.Update_Events_Queue.before.invoke_internal(ctx)

        self.entities.update()

        self.handler.Global_Events.State_Events.Update_Events_Queue.after.invoke_internal(
            ctx)
        self.events_handler.State_Events.Update_Events_Queue.after.invoke_internal(ctx)

    def draw_on(self, surf: pygame.Surface) -> None:
        ctx = State_EventContext(self, self.events_handler.State_Events.Draw_Events_Queue)

        if debugger.FLAGS.debug and debugger.FLAGS.state_context_info:
            print("context:", ctx)

        self.handler.Global_Events.State_Events.Draw_Events_Queue.before.invoke_internal(
            ctx)
        self.events_handler.State_Events.Draw_Events_Queue.before.invoke_internal(ctx)

        self.entities.draw_on(surf)

        self.handler.Global_Events.State_Events.Draw_Events_Queue.after.invoke_internal(
            ctx)
        self.events_handler.State_Events.Draw_Events_Queue.after.invoke_internal(ctx)


class States:
    Global_Events = EventsHandler()

    def __init__(self, handler: Optional[Game] = None) -> None:
        self.prev_state: Optional[State] = None

        self.game_handler = handler
        self.deque: deque[State] = deque()

        self.default_state = State(self)
        self.active_state = self.default_state

        self.deque.append(self.default_state)
        self.default_state.events_handler.Pygame_Event.actions.register(
            pygame.QUIT, QUIT)

    def activate_previous_state(self):
        if self.prev_state is None:
            raise NoPreviousStates("Can not rollback on first state")

        if debugger.FLAGS.debug and debugger.FLAGS.states_transitions:
            print(f"Switching state from: {self.active_state} to {self.prev_state}")

        self.active_state = self.prev_state
        self.deque.appendleft(self.prev_state)
        self.prev_state = None

    def activate_next_state(self):
        self.prev_state = self.active_state or self.default_state

        try:
            self.active_state = self.deque.pop()
        except IndexError:
            raise NoMoreStates("No states left in queue") from None

        if debugger.FLAGS.debug and debugger.FLAGS.states_transitions:
            print(f"Switching state from: {self.prev_state} to {self.active_state}")

    def __bool__(self):
        return bool(self.deque)


    

@States.Global_Events.Pygame_Event.actions.decorator_register(pygame.QUIT)
def QUIT(ctx: State_EventContext):
    ctx.active_state.running = False
    print("Quitting...")
    return debugger.show_log("Quitting...")


if __name__ == '__main__':
    states = States()

    def test_push_pop():
        state = State(states)

    test_push_pop()
