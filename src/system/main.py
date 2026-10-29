import math
from typing import Optional

import pygame
from pygame.key import ScancodeWrapper
from pygame.event import Event

from pathlib import Path

from helper import debug, env
from helper.logger import notifications
from state import NoMoreStates, States,State
from graphics import Window, Background  # type: ignore

from helper.logger import show_message

class movement_handler:
    def __init__(self, handler: Game) -> None:
        self.game_handler = handler

    @property
    def distance_error_amount(self):
        "Convert ms to seconds for the final distance calculation"
        return self.game_handler.window.clock.dt 

    def right(self, velocity: float) -> float:
        return self.distance_error_amount * velocity

    def left(self, velocity: float) -> float:
        return self.distance_error_amount * velocity

    def up(self, velocity: float) -> float:
        return self.distance_error_amount * velocity

    def down(self, velocity: float) -> float:
        return self.distance_error_amount * velocity

    def calculate_diagonal_movement(self, right: float, up: float):
        # Calculate the total length of the input vector
        length = math.sqrt(right**2 + up**2)

        # If moving diagonally, length will be ~1.414.
        # Dividing by length scales right and up down to ~0.7071 each.
        if length > 0:
            right /= length
            up /= length

        # Distance = Normalized Direction * Speed * Time
        distance_x = right * self.distance_error_amount
        distance_y = up * self.distance_error_amount

        return distance_x, distance_y

    class straight[Number:int | float]:
        @staticmethod
        def right(handler_engine: movement_handler, amount: Number) -> float:
            return handler_engine.distance_error_amount * amount

        @staticmethod
        def left(handler_engine: movement_handler, amount: Number) -> float:
            return handler_engine.distance_error_amount * amount

        @staticmethod
        def up(handler_engine: movement_handler, amount: Number) -> float:
            return handler_engine.distance_error_amount * amount

        @staticmethod
        def down(handler_engine: movement_handler, amount: Number) -> float:
            return handler_engine.distance_error_amount * amount


class Game:
    def __init__(self, window_name: str = "Window", background: Optional[Background] = None, target_fps: float = 0) -> None:
        notifications.NotificationMessages.init.display()

        self.States = States().with_handler(self)
        self.DEFAULT_STATE = self.States.default_state

        self.window = Window(
            name=window_name,
            background_handler=background,
            fps_target=target_fps)

        env.load_debug_settings()

        notifications.NotificationMessages.init_done.display()

    def get_inputs(self):
        keys_stream: ScancodeWrapper = pygame.key.get_pressed()
        keys_pressed: ScancodeWrapper = pygame.key.get_just_pressed()
        triggered_events: list[Event] = pygame.event.get()
        return triggered_events, keys_stream, keys_pressed

    def run_logic(self, state: State):
        if debug.FLAGS.states_info and debug.FLAGS.detailed_info:
            print("Handling logic...")

        triggered_events, keys_stream, keys_pressed = self.get_inputs()

        state.handle_keyboard_input(
            keys_pressed=keys_pressed, keys_stream=keys_stream)

        state.handle_pygame_events(triggered_events)

        if debug.FLAGS.debug_mode and debug.FLAGS.states_info and debug.FLAGS.detailed_info:
            print("Finished logic.")
            print("Updating state...")

    def setUp(self):
        notifications.NotificationMessages.welcome.display()
        if not self.States:
            if debug.FLAGS.states_transitions:
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
        if debug.FLAGS.debug_mode and debug.FLAGS.states_info:
            print("State update finished.")
            print("Updating window...")

        self.window.update()
        if debug.FLAGS.debug_mode and debug.FLAGS.states_info and debug.FLAGS.detailed_info:
            print("window update finished.")
            print("Drawing...")

    def draw(self, state: State):

        self.window.draw(state)
        if debug.FLAGS.debug_mode and debug.FLAGS.states_info and debug.FLAGS.detailed_info:
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

            if debug.FLAGS.run_once is True:
                break

        notifications.NotificationMessages.goodbye.display()

    run = game_loop


if __name__ == '__main__':
    def test1():
        from helper import debug
        # debug.FLAGS.set_all(True)

        game = Game()

        # game.DEFAULT_STATE.running = False# DEBUG
        # debugger.debug.run_once = True
        game.run()
    test1()
