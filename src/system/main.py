import math
from typing import Optional

import pygame
from pygame.key import ScancodeWrapper
from pygame.event import Event

from pathlib import Path

from helper.env import load_debug_settings as env_load_debug_settings
from helper.debugger import FLAGS
from helper.logger import notifications, show_message

from state import NoMoreStates, States, State
from graphics import Window, Background


class Game:
    def __init__(self, window_name: str = "Window", background: Optional[Background] = None, target_fps: float = 0) -> None:
        notifications.NotificationMessages.init.display()

        self.States = States().with_handler(self)
        self.DEFAULT_STATE = self.States.default_state

        self.window = Window(
            name=window_name,
            background_handler=background,
            fps_target=target_fps)

        env_load_debug_settings()

        notifications.NotificationMessages.init_done.display()

    def get_inputs(self):
        keys_stream: ScancodeWrapper = pygame.key.get_pressed()
        keys_pressed: ScancodeWrapper = pygame.key.get_just_pressed()
        triggered_events: list[Event] = pygame.event.get()
        return triggered_events, keys_stream, keys_pressed

    def run_logic(self, state: State):
        if FLAGS.states_info and FLAGS.detailed_info:
            print("Handling logic...")

        triggered_events, keys_stream, keys_pressed = self.get_inputs()

        state.handle_keyboard_input(
            keys_pressed=keys_pressed, keys_stream=keys_stream)

        state.handle_pygame_events(triggered_events)

        if FLAGS.debug_mode and FLAGS.states_info and FLAGS.detailed_info:
            print("Finished logic.")
            print("Updating state...")

    def setUp(self):
        notifications.NotificationMessages.welcome.display()
        if not self.States:
            if FLAGS.states_transitions:
                print("No states found.")
                print("Using Default State.")
            self.States.deque.append(self.States.default_state)

        self.States.activate_next_state()
        # self.States.prev_state = None  # remove default state from

    def optimize_game(self):
        ...
        # TODO implement

    def update(self, state: State):
        state.update(self.window.clock.dt)
        if FLAGS.debug_mode and FLAGS.states_info:
            print("State update finished.")
            print("Updating window...")

        self.window.update()
        if FLAGS.debug_mode and FLAGS.states_info and FLAGS.detailed_info:
            print("window update finished.")
            print("Drawing...")

    def draw(self, state: State):

        self.window.draw(state)
        if FLAGS.debug_mode and FLAGS.states_info and FLAGS.detailed_info:
            print("Finished Drawing.")

    def game_loop(self):
        self.setUp()

        active_state = self.States.active_state

        while active_state.running:
            """
             TODO IMPLEMENT:
             ! HALTING AND SKIPPING SYSTEM
             ! FOR ACTIONS PERFORMED BY DISPATCHED CALLBACKS
             ! ex: if state.running=False; pick if you want to skip all events or just this loop
             ! make logic_events_dispatchers that run automatically above normal events and can be skipped too via special option"""

            active_state: State = self.States.active_state

            self.window.clock.tick()

            self.run_logic(active_state)

            self.update(active_state)

            self.draw(active_state)

            if FLAGS.run_once is True:
                break

        notifications.NotificationMessages.goodbye.display()

    run = game_loop


if __name__ == '__main__':
    def test1():
        from helper import debugger
        # debug.FLAGS.set_all(True)

        game = Game()

        # game.DEFAULT_STATE.running = False# DEBUG
        # debugger.debug.run_once = True
        game.run()
    test1()
