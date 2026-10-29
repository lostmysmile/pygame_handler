from typing import Iterable



class FLAGS:
    __slots__ = ()

    run_once = False
    debug_mode = False
    detailed_info = False
    event_info = False
    init_info = False
    event_registers = False
    states_info = False
    state_context_info = False
    states_transitions = False

    # TODO ADD TIMERS FOR PROFILING EACH STEP OF THE CODE
    time_internals = False

    @classmethod
    def set(cls, bunch: Iterable[str], state: bool = False):
        expected_error = ValueError(f"Invalid argument entered: {bunch!r}")
        assert isinstance(bunch, (Iterable, str)), expected_error
        for k in bunch:
            try:
                v = getattr(cls, k)
            except AttributeError as e:
                expected_error.add_note(f"flag not found: {k!r}")
                raise expected_error from e
            if isinstance(v, bool):
                setattr(cls, k, state)
            else:
                raise ValueError("Invalid config")

    @classmethod
    def set_all(cls, state: bool = False):
        for k, v in cls.__dict__.items():
            if isinstance(v, bool):
                setattr(cls, k, state)


