import math
from typing import Optional

import pygame
from pygame.key import ScancodeWrapper
from pygame.event import Event

from pathlib import Path

from pygame_handler.helper.env import load_debug_configs as env_load_debug_configs
from pygame_handler.helper.debugger import FLAGS
from pygame_handler.helper.logger import notification_system

from pygame_handler.helper.logger import show_message
from pygame_handler.scene import NoMoreStates, Scenes_handler
from pygame_handler.scene import Scene
from pygame_handler.graphics import Window, Background


class Game:
    def __init__(self, window_name: str = "Window", background: Optional[Background] = None, target_fps: float = 0) -> None:
        notification_system.Notification.init.display()

        self.States = Scenes_handler().with_handler(self)
        self.DEFAULT_STATE = self.States.default_state

        self.window = Window(
            name=window_name,
            background_handler=background,
            fps_target=target_fps)

        env_load_debug_configs()

        notification_system.Notification.init_done.display()

    def get_inputs(self):
        keys_stream: ScancodeWrapper = pygame.key.get_pressed()
        keys_pressed: ScancodeWrapper = pygame.key.get_just_pressed()
        triggered_events: list[Event] = pygame.event.get()
        return triggered_events, keys_stream, keys_pressed

    def run_logic(self, state: Scene):
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
        notification_system.Notification.welcome.display()
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

    def update(self, state: Scene):
        state.update(self.window.clock.dt)
        if FLAGS.debug_mode and FLAGS.states_info:
            print("State update finished.")
            print("Updating window...")

        self.window.update()
        if FLAGS.debug_mode and FLAGS.states_info and FLAGS.detailed_info:
            print("window update finished.")
            print("Drawing...")

    def draw(self, state: Scene):

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

            active_state: Scene = self.States.active_state

            self.window.clock.tick()

            self.run_logic(active_state)

            self.update(active_state)

            self.draw(active_state)

            if FLAGS.run_once is True:
                break

        notification_system.Notification.goodbye.display()

    run = game_loop


if __name__ == '__main__':
    def test1():
        from pygame_handler.helper import debugger
        # debugger.FLAGS.set_all(True)

        game = Game()

        # game.DEFAULT_STATE.running = False# DEBUG
        # debugger.debug.run_once = True
        # @game.DEFAULT_STATE.events_handler.Pygame_Event.register_decorator(1)
        # def testing():print("hello wolrd")

        game.run()
    test1()
