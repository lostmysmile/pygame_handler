from itertools import chain
from typing import Self
from pygame.key import ScancodeWrapper
from collections import deque
from typing import Optional


import pygame

from pathlib import Path


if __package__:
    from sys import path as sys_path
    from .events import EventsHandler, State_EventContext, ENUMS as EVENT_NUMS
    from ..graphics import EntitiesHandler
else:
    # from system import Default_Entity
    from sys import path as sys_path
    sys_path.append( Path(__file__).parent.parent.as_posix())
    print(sys_path)
    from system.state.events import EventsHandler, State_EventContext, ENUMS as EVENT_NUMS
    from graphics import EntitiesHandler


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
        # self.global_events.Keyboard_Event
        # self.local_events.Keyboard_Event
        # raise NotImplementedError()
        pass  # Default: do nothing

    def handle_pygame_events(self, pygame_events) -> None:
        (ctx := self.events_handler.Pygame_Event.context).active_state = self

        if not pygame_events:
            return

        handled = set()
        events_and_listeners = chain(
            States.Global_Events.Pygame_Event.Events_List,
            self.events_handler.Pygame_Event.Events_List)

        if self.handler.game_handler.DEBUG_MODE:
            print(f"Active pygame events: {pygame_events!r}")
        print(events_and_listeners)

        for event_trigger, listeners in events_and_listeners:
            if not listeners:
                continue
            if self.handler.game_handler.DEBUG_MODE:
                if event_trigger != EVENT_NUMS.ANY_TRIGGER:
                    print(f"Checking: {event_trigger!r}, {listeners!r}")

            if (event_trigger == EVENT_NUMS.ANY_TRIGGER) or (pygame.Event(event_trigger) in pygame_events):
                for listener in listeners:
                    if listener.handle_once is True and listener.action in handled:
                        if self.handler.game_handler.DEBUG_MODE:
                            print(
                                f"Skipped {listener.action!r}; Has already been triggered")
                        continue

                    if self.handler.game_handler.DEBUG_MODE:
                        if event_trigger == EVENT_NUMS.ANY_TRIGGER:
                            print(
                                f"handling <GENERIC_TRIGGER>{EVENT_NUMS.ANY_TRIGGER!r}",
                                end=" with",
                            )
                        else:
                            assert isinstance(event_trigger, int)
                            print(
                                f"handling {pygame.event.event_name(event_trigger)!r}"
                                f"({event_trigger})",
                                end=" with",
                            )

                        print(f"{listener}.")

                    if self.handler.game_handler.DEBUG_MODE:
                        print(
                            f"Triggering: {listener.action!r} <HANDLE_ONCE={listener.handle_once!r}>")

                    listener.action(ctx)
                    if listener.handle_once:
                        handled.add(listener.action)

        #         for event in pygame_events:
        #             if listener.trigger == event.type:
        #         else:
        #             continue

        #     if __debug__:
        #         print(f"{listener}.")
        #     listener.action(ctx)
        #     if listener.handle_once:
        #         handled.add(listener.action)
        # raise NotImplementedError()

    def update(self, dt: float) -> None:
        return  # TODO REMOVE LATER
        if self.handler.game_handler.DEBUG_MODE:
            print("Updating...")
        self.events_handler.State_Events.Update_Event.before_render.context.update(
            active_state=self, dt=dt)

        self.handler.Global_Events.State_Events.Update_Event.before_render.invoke_internal()
        self.events_handler.State_Events.Update_Event.before_render.invoke_internal()

        self.entities.update()

        self.handler.Global_Events.State_Events.Update_Event.after_render.invoke_internal()
        self.events_handler.State_Events.Update_Event.after_render.invoke_internal()
        if self.handler.game_handler.DEBUG_MODE:
            print("Finished updating.")

    def draw(self, surf: pygame.Surface) -> None:
        return  # TODO REMOVE LATER
        if self.handler.game_handler.DEBUG_MODE:
            print("Drawing...")

        self.events_handler.State_Events.Draw_Event.before_render.context.active_state = self

        self.handler.Global_Events.State_Events.Draw_Event.before_render.invoke_internal()
        self.events_handler.State_Events.Draw_Event.before_render.invoke_internal()

        self.entities.draw(surf)

        self.handler.Global_Events.State_Events.Draw_Event.after_render.invoke_internal()
        self.events_handler.State_Events.Draw_Event.after_render.invoke_internal()

        if self.handler.game_handler.DEBUG_MODE:
            print("Finished Drawing.")


class States:
    Global_Events = EventsHandler()

    def __init__(self, handler: "Game" | None = None) -> None:
        self.prev_state: Optional[State] = None

        self.game_handler = handler
        self.deque: deque[State] = deque()

        self.default_state = State(self)
        self.active_state = self.default_state

        self.deque.append(self.default_state)
        print("registered")
        self.default_state.events_handler.Pygame_Event.Events_List.register(
            pygame.QUIT, QUIT)

    def activate_previous_state(self):
        if self.prev_state is None:
            raise NoPreviousStates("Can not rollback on first state")
        if self.game_handler.DEBUG_MODE:
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

        if self.game_handler.DEBUG_MODE:
            print(f"Switching state from: {self.prev_state} to {self.active_state}")

    def __bool__(self):
        return bool(self.deque)


@States.Global_Events.Pygame_Event.Events_List.decorator_register()
def QUIT(ctx: State_EventContext):
    ctx.active_state.running = False
    print("ByeBye!")


if __name__ == '__main__':
    states = States()

    def test_push_pop():
        state = State(states)

    test_push_pop()
