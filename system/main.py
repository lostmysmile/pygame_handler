from typing import Optional

import pygame
from pygame.key import ScancodeWrapper
from pygame.event import Event

from pathlib import Path

if __package__:
    from .state import State, States, NoMoreStates  # type: ignore
    from .graphics import Window, Background  # type: ignore
else:
    from sys import path as sys_path
    sys_path.insert(0, Path(__file__).parent.parent.as_posix())
    from state import State, States, NoMoreStates  # type: ignore
    from graphics import Window, Background  # type: ignore


class Game:
    DEBUG_MODE: bool = False

    def __init__(self, window_name: str = "Window", background: Optional[Background] = None, target_fps: float = 0) -> None:
        self.States = States(self)
        self.DEFAULT_STATE = self.States.default_state

        self.window = Window(
            name=window_name,
            background_handler=background,
            fps_target=target_fps)

    def loop_logic(self):
        active_state = self.States.active_state
        pressed_keys: ScancodeWrapper = pygame.key.get_pressed()
        active_state.handle_keyboard_input(keys=pressed_keys)

        triggered_events: list[Event] = pygame.event.get()
        active_state.handle_pygame_events(triggered_events)

        active_state.update(self.window.clock.dt)

    def run(self):
        if self.States:
            self.States.activate_next_state()
            self.States.prev_state = None  # remove default state from deque

        active_state = self.States.active_state

        while active_state.running:
            # TODO implement
            self.loop_logic()
            self.window.update()
            self.window.draw(active_state)


if __name__ == '__main__':
    def test1():
        game = Game()
        game.run()
    test1()
