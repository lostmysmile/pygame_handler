from itertools import chain
from typing import NoReturn
from pygame.key import ScancodeWrapper
from pygame.event import Event
from collections import deque
from typing import Optional


import pygame

from pathlib import Path

from system.state.events import State_EventContext, PygameEvents

if __package__:
    from .events import EventsHandler, State_EventContext, ENUMS as EVENT_NUMS
    from ..graphics import EntitiesHandler
else:
    # from system import Default_Entity
    from sys import path as sys_path
    sys_path.insert(0, Path(__file__).parent.parent.as_posix())
    from events import EventsHandler, State_EventContext, ENUMS as EVENT_NUMS
    from graphics import EntitiesHandler


class NoMoreStates(StopIteration):
    ...


class NoPreviousStates(StopIteration):
    ...


class State:
    def __init__(self, handler: "States") -> None:
        self.running = True
        self.handler = handler
        self.entities = EntitiesHandler()
        self.events_handler = EventsHandler()

    def handle_keyboard_input(self, keys: ScancodeWrapper) -> None:
        # self.global_events.Keyboard_Event
        # self.local_events.Keyboard_Event
        # raise NotImplementedError()
        pass  # Default: do nothing

    def handle_pygame_events(self, pygame_events) -> None:
        ctx: State_EventContext[PygameEvents] = self.events_handler.Pygame_Event.context
        ctx.active_state = self
        # for event in pygame_events:
        #     print(event)
        #     for listener in self.events_handler.Pygame_Event.Events_List:
        #         if (event.type == (listener.trigger)):
        #             listener.action(ctx)

        handled = set()
        listeners = chain(self.handler.Global_Events.Pygame_Event.Events_List,
                          self.events_handler.Pygame_Event.Events_List)

        for listener in listeners:
            if listener.handle_once is True and listener.action in handled:
                continue
            if listener.trigger != EVENT_NUMS.ANY_TRIGGER:
                for event in pygame_events:
                    if listener.trigger == event.type:
                        if __debug__:
                            print("Debug: handling", event, end="with")
                        break
                else:
                    continue

            if __debug__:
                print(f"{listener}.")
            listener.action(ctx)
            if listener.handle_once:
                handled.add(listener.action)
        # raise NotImplementedError()

    def update(self, dt: float) -> None:
        self.events_handler.State_Events.Update_Event.before_render.context.update(
            active_state=self, dt=dt)

        self.handler.Global_Events.State_Events.Update_Event.before_render.invoke_internal()
        self.events_handler.State_Events.Update_Event.before_render.invoke_internal()

        self.entities.update()

        self.handler.Global_Events.State_Events.Update_Event.after_render.invoke_internal()
        self.events_handler.State_Events.Update_Event.after_render.invoke_internal()

    def draw(self, surf: pygame.Surface) -> None:
        self.events_handler.State_Events.Draw_Event.before_render.context.active_state = self

        self.handler.Global_Events.State_Events.Draw_Event.before_render.invoke_internal()
        self.events_handler.State_Events.Draw_Event.before_render.invoke_internal()

        self.entities.draw(surf)

        self.handler.Global_Events.State_Events.Draw_Event.after_render.invoke_internal()
        self.events_handler.State_Events.Draw_Event.after_render.invoke_internal()


class States:
    prev_state: Optional[State] = None

    def __init__(self) -> None:
        self.deque: deque[State] = deque()
        self.Global_Events = EventsHandler()

        self.default_state = State(self)
        self.active_state = self.default_state

        self.deque.append(self.default_state)
        print("registered")
        self.default_state.events_handler.Pygame_Event.Events_List.register(
            pygame.QUIT, QUIT)

    def activate_previous_state(self):
        if self.prev_state is None:
            raise NoPreviousStates("Can not rollback on first state")

        self.active_state = self.prev_state
        self.deque.appendleft(self.prev_state)
        self.prev_state = None

    def activate_next_state(self):
        self.prev_state = self.active_state or self.default_state

        try:
            self.active_state = self.deque.pop()
        except IndexError:
            raise NoMoreStates("No states left in queue") from None

    def __bool__(self):
        return bool(self.deque)


def QUIT(ctx: State_EventContext):
    ctx.active_state.running = False
    print("ByeBye!")


if __name__ == '__main__':
    states = States()

    def test_push_pop():
        state = State(states)

    test_push_pop()
