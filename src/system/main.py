import math
from typing import Optional

import pygame
from pygame.key import ScancodeWrapper
from pygame.event import Event

from pathlib import Path

from helper import debugger
from .state import State, States, NoMoreStates  # type: ignore
from .graphics import Window, Background  # type: ignore


class movement_handler:
    def __init__(self, handler: Game) -> None:
        self.game_handler = handler

    @property
    def distance_error_amount(self):
        "Convert ms to seconds for the final distance calculation"
        return self.game_handler.window.clock.dt / 1000

    def right(self, amount: float) -> float:
        return self.distance_error_amount * amount

    def left(self, amount: float) -> float:
        return self.distance_error_amount * amount

    def up(self, amount: float) -> float:
        return self.distance_error_amount * amount

    def down(self, amount: float) -> float:
        return self.distance_error_amount * amount

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
    class Settings:
        __slots__ = ()
        speed_multiplier = 1

    def __init__(self, window_name: str = "Window", background: Optional[Background] = None, target_fps: float = 0) -> None:
        if debugger.settings.init:
            print("Initializing...")

        self.States = States().with_handler(self)
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
        if not self.States:
            if debugger.FLAGS.states_transitions:
                print("No states found.")
                print("Using Default State.")
            self.States.deque.append(self.States.default_state)

        self.States.activate_next_state()
        # self.States.prev_state = None  # remove default state from 


        active_state = self.States.active_state

        while active_state.running:
            """
             TODO IMPLEMENT:
             ! HALTING AND SKIPPING SYSTEM
             ! FOR ACTIONS PERFORMED BY DISPATCHED CALLBACKS
             ! ex: if state.running=False; pick if you want to skip all events or just this loop
             ! make logic_events_dispatchers that run automatically above normal events and can be skipped too via special option"""

            self.window.clock.tick()

            if debugger.FLAGS.states_info and debugger.FLAGS.detailed_info:
                print("Handling logic...")

            self.main_logic()
            if debugger.FLAGS.debug and debugger.FLAGS.states_info and debugger.FLAGS.detailed_info:
                print("Finished logic.")
                print("Updating state...")

            active_state.update(self.window.clock.dt)
            if debugger.FLAGS.debug and debugger.FLAGS.states_info:
                print("State update finished.")
                print("Updating window...")

            self.window.update()
            if debugger.FLAGS.debug and debugger.FLAGS.states_info and debugger.FLAGS.detailed_info:
                print("window update finished.")
                print("Drawing...")

            self.window.draw(active_state)
            if debugger.FLAGS.debug and debugger.FLAGS.states_info and debugger.FLAGS.detailed_info:
                print("Finished Drawing.")

            if debugger.debug.run_once is True:
                break

        if debugger.settings.goodbye:
            print("Bye bye!")

    run = run_loop


if __name__ == '__main__':
    def test1():
        game = Game()

        # game.DEFAULT_STATE.running = False# DEBUG
        from helper import debugger
        debugger.FLAGS.set_all(True)
        debugger.debug.run_once = True
        game.run_loop()
    test1()
