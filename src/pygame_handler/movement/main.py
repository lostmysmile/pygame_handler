import math

from pygame_handler.graphics import clock_handler

class movement_handler:
    def __init__(self, clock: clock_handler) -> None:
        self.clock_handler: clock_handler = clock

    @property
    def distance_error_amount(self) -> float:
        "Convert ms to seconds for the final distance calculation"
        return self.clock_handler.dt 

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