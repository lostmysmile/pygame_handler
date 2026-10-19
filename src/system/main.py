from typing import Optional

import pygame
from pygame.key import ScancodeWrapper
from pygame.event import Event

from pathlib import Path

from helper import debugger
from .state import State, States, NoMoreStates  # type: ignore
from .graphics import Window, Background  # type: ignore


class Game:

    def __init__(self, window_name: str = "Window", background: Optional[Background] = None, target_fps: float = 0) -> None:
        if debugger.settings.init:
            print("Initializing...")

        self.States = States(self)
        self.DEFAULT_STATE = self.States.default_state

        self.window = Window(
            name=window_name,
            background_handler=background,
            fps_target=target_fps)

        if debugger.settings.init:
            print("Finished initializing")

    def main_logic(self):
        active_state = self.States.active_state
        pressed_keys: ScancodeWrapper = pygame.key.get_pressed()
        active_state.handle_keyboard_input(keys=pressed_keys)

        triggered_events: list[Event] = pygame.event.get()
        active_state.handle_pygame_events(triggered_events)

    def run_loop(self):
        if self.States:
            self.States.activate_next_state()
            self.States.prev_state = None  # remove default state from deque

            if debugger.FLAGS.states_transitions:
                print("Using user-defined State:", self.States.active_state)
                print("Removed Default state.")
        else:
            if debugger.FLAGS.states_transitions:
                print("Using Default State.")

        active_state = self.States.active_state

        while active_state.running:
            if debugger.FLAGS.states_info and debugger.FLAGS.detailed_info:
                print("Handling logic...")
            self.main_logic()

            if debugger.FLAGS.debug and debugger.FLAGS.states_info and debugger.FLAGS.detailed_info:
                print("Finished logic.")

            if debugger.FLAGS.debug and debugger.FLAGS.states_info and debugger.FLAGS.detailed_info:
                print("Updating...")
            active_state.update(self.window.clock.dt)

            if debugger.FLAGS.debug and debugger.FLAGS.states_info:
                print("Updated.")
            self.window.update()

            if debugger.FLAGS.debug and debugger.FLAGS.states_info and debugger.FLAGS.detailed_info:
                print("Drawing...")
            self.window.draw(active_state)

            if debugger.FLAGS.debug and debugger.FLAGS.states_info and debugger.FLAGS.detailed_info:
                print("Finished Drawing.")

        if debugger.settings.goodbye:
            print("Bye bye!")

    run = run_loop


if __name__ == '__main__':
    def test1():
        game = Game()

        # game.DEFAULT_STATE.running = False# DEBUG
        from helper import debugger
        debugger.FLAGS.set_all(True)
        game.run_loop()
    test1()
