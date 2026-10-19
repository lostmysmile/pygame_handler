from functools import wraps

import keyboard
from pathlib import Path
import time
from typing import Any, Callable, Literal, Optional, TypeVar, ParamSpec


def load_file(filename: str, Directory: Path | str = ""):
    filepath = Path(Directory)/filename
    assert filepath.exists(), 'file {!r} does not exist in {!r}'.format(
        filepath.name, filepath.parent.absolute())
    return filepath.absolute()


class Result[B, T]:
    __slots__ = "success", "value"

    def __init__(self, is_ok: B, value: T) -> None:
        self.success = is_ok
        self.value = value

    def __bool__(self) -> B:
        return self.success

    def get_result(self) -> tuple[B, T]:
        return self.success, self.value

    def __iter__(self):
        return iter(self.get_result())


P = ParamSpec("P")
R = TypeVar("R")


class cooldown:
    def __init__(self, interval: float, first_check_result: bool = True):
        self._timers: dict[Any, float] = {}
        self.interval: float = interval
        self.first_result: bool = first_check_result

    def reset_timer(self, item: Optional[Any] = None):
        del self._timers[item]

    def reset_all_timers(self):
        self._timers.clear()

    def has_passed(self, item: Optional[Any] = None) -> bool:
        now: float = time.perf_counter()

        try:
            last_time = self._timers[item]
        except KeyError:
            self._timers[item] = now
            return self.first_result

        status: bool = ((now - last_time) >= self.interval )
        if (status):
            self._timers[item]= now

        return status

    def assign_cooldown(self, func: Callable[P, R]):

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[Literal[True], R] | Result[Literal[False], None]:
            if self.has_passed(id(func)):
                result = func(*args, **kwargs)
                outcome = Result[Literal[True], R](True, result)
                return outcome
            else:
                outcome = Result[Literal[False], None](False, None)
                return outcome
        return wrapper

    def copy(self):
        return cooldown(self.interval, self.first_result)


if __name__ == '__main__':
    cd1 = cooldown(.5)
    cd2 = cd1.copy()

    @cd1.assign_cooldown
    def greet(to: str):
        return ("hello" + to)

    while not keyboard.is_pressed("esc"):
        result = greet("person").get_result()
        if result[0] is True:
            k = result
            print("greet", k)
        else:
            k = result
    print('"esc" pressed')

    # exit()
    a, b = 1, 2
    print(cd2.has_passed(1))

    while not keyboard.is_pressed("enter"):
        if cd2.has_passed(1):
            print('1')
        if cd2.has_passed(2):
            print('2')
    print('"enter" pressed')
    while not keyboard.is_pressed("f"):
        if cd2.has_passed():
            print('passed', cd2._timers)  # pyright: ignore[reportPrivateUsage]
    print('"f" pressed')

    # print(load_file(".vscode").absolute())
    # print(load_file(".vscode", ("pictures", "secrets")))
    # print(load_file("something","somewhere"))
