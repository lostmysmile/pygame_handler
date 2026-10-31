from __future__ import annotations
from ordered_set import OrderedSet

from collections import defaultdict, namedtuple
from collections.abc import Callable, Generator, Iterable
from typing import TYPE_CHECKING, Any, LiteralString, Self, Unpack, cast
import pygame


if TYPE_CHECKING:
    from .. import Scene


from . import ENUMS

type Trigger = int | ENUMS.TRIGGERS


class EventContext:
    __slots__ = ()


class StateEventContext[EventT](EventContext):
    __slots__ = ("triggered_event", "active_state", "dt")

    def __init__(
        self,
        active_state: Scene,
        triggered_event: EventT | None = None,
        dt: float | None = None,
    ) -> None:
        self.active_state = active_state
        self.triggered_event: EventT | None = triggered_event
        self.dt = dt

    def __str__(self) -> str:
        return (
            f"<StateEventContext["
            f"state={self.active_state}, "
            f"event={self.triggered_event!r}, "
            f"dt={self.dt}]>"
        )


class DrawEventContext(EventContext):
    __slots__ = ("active_state")

    def __init__(self, active_state: Scene) -> None:
        self.active_state: Scene = active_state

    def __str__(self) -> str:
        return f"<DrawEventContext[state={self.active_state}]"

    def update(self, active_state):
        self.active_state = active_state


class CallbackInfo[**P, R]:
    __slots__ = "action", "invocation_policy"

    def __init__(self,
                 action: Callable[P, R],
                 invocation_policy: ENUMS.invocation_policy = ENUMS.invocation_policy.ONCE_PER_LOOP,
                 ):
        assert action is not None, "Action can not be None"
        self.action: Callable[P, R] = action
        self.invocation_policy: ENUMS.invocation_policy = invocation_policy

    def __str__(self):
        return f"<{self.action!r} policy={self.invocation_policy}>"

    def __iter__(self):
        yield self.action
        yield self.invocation_policy


class Callbacks[ContextT, R= Any]:
    __slots__ = ("registered_actions",)

    def __init__(self, *,
                 custom_registered_iterable: Iterable[CallbackInfo[[ContextT], R]] | None = None) -> None:
        assert isinstance(custom_registered_iterable,
                          Iterable) or custom_registered_iterable is None, custom_registered_iterable

        self.registered_actions: OrderedSet[
            CallbackInfo[[ContextT], R]
        ] = OrderedSet(custom_registered_iterable or [])

    def __iter__(self):
        yield from self.registered_actions

    def __len__(self):
        return len(self.registered_actions)

    def _iterable_invoke_all(self, ctx: ContextT) -> Generator[tuple[CallbackInfo[[ContextT], R], R], Any, None]:
        for info in self.registered_actions:
            yield (info, info.action(ctx))

    def _invoke_all(self, ctx: ContextT) -> None:
        for info in self.registered_actions:
            info.action(ctx)

    def __ror__(self: Callbacks[ContextT, R], other: Callbacks[ContextT, R] | None) -> Callbacks[ContextT, R]:
        return Callbacks.__or__(self, other)

    def __or__(self: Callbacks, other: Callbacks[ContextT, R] | None) -> Callbacks[ContextT, R]:
        if not other:
            return self
        new_list = self.registered_actions | other.registered_actions
        return Callbacks(custom_registered_iterable=new_list)

    def register(
        self,
        action: Callable[[ContextT], R],
        invocation_policy: ENUMS.invocation_policy
        = ENUMS.invocation_policy.ONCE_PER_LOOP,
    ) -> Callable[[ContextT], R]:
        info = CallbackInfo(
            action,
            invocation_policy=invocation_policy,
        )

        self._register_info(info)

        return action

    def _register_info(
        self,
        info: CallbackInfo[[ContextT], R],
    ) -> None:

        self.registered_actions.add(info)


class EventsDict[
    TriggerT:int | ENUMS.TRIGGERS,
    EventT,
    ReturnT= Any,
]:
    __slots__ = ("registered_actions",)

    def __init__(self) -> None:
        self.registered_actions: defaultdict[
            TriggerT,
            Callbacks[StateEventContext[EventT], ReturnT],
        ] = defaultdict(
            Callbacks[StateEventContext[EventT], ReturnT]
        )

    def _register_info(
        self,
        trigger: TriggerT,
        info: CallbackInfo[
            [StateEventContext[EventT]],
            ReturnT,
        ],
    ) -> None:
        if not (
            type(trigger) is int
            or isinstance(trigger, ENUMS.TRIGGERS)
        ):
            raise TypeError(f"Unknown trigger type: {trigger!r}")

        self.registered_actions[trigger]._register_info(info)

    def _register_internal(
        self,
        trigger: TriggerT,
        func: Callable[[StateEventContext[EventT]], ReturnT],
        invocation_policy: ENUMS.invocation_policy = ENUMS.invocation_policy.ONCE_PER_LOOP,
    ) -> Callable[[StateEventContext[EventT]], ReturnT]:

        if not (
            type(trigger) is int
            or isinstance(trigger, ENUMS.TRIGGERS)
        ):
            raise TypeError(f"Unknown trigger type: {trigger!r}")

        if not callable(func):
            raise TypeError(f"Expected callable for func, got: {func!r}")

        info = CallbackInfo(
            action=func,
            invocation_policy=invocation_policy,
        )

        self._register_info(trigger, info)

        return func

    def register(
        self,
        triggers: TriggerT | Iterable[TriggerT],
        func: Callable[[StateEventContext[EventT]], ReturnT],
        invocation_policy: ENUMS.invocation_policy
        = ENUMS.invocation_policy.ONCE_PER_LOOP,
    ) -> Callable[[StateEventContext[EventT]], ReturnT]:
        """Register a callback for one or multiple triggers."""
        if not callable(func):
            raise TypeError(f"Expected callable for func, got: {func!r}")
            
        if  isinstance(triggers, (int,ENUMS.TRIGGERS)):
            triggers_to_register: Iterable[TriggerT] = (cast(TriggerT, triggers),)
        elif not isinstance(triggers, (str, Iterable)):
            raise TypeError(
                f"Expected a trigger or iterable of triggers, got: {triggers!r}"
            )
        else:

            triggers_to_register = cast(
                Iterable[TriggerT],
                triggers,
            )

        info = CallbackInfo(
            func,
            invocation_policy=invocation_policy,
        )

        for trigger in triggers_to_register:
            self._register_info(trigger, info)

        return func

    def decorator_register(
        self,
        trigger: TriggerT,
        invocation_policy: ENUMS.invocation_policy
        = ENUMS.invocation_policy.ONCE_PER_LOOP,
    ):
        """Return a decorator that registers a callback for a trigger."""

        def decorator(
            func: Callable[[StateEventContext[EventT]], ReturnT],
        ) -> Callable[[StateEventContext[EventT]], ReturnT]:
            return self._register_internal(
                trigger,
                func,
                invocation_policy,
            )

        return decorator

    def register_decorator(
        self,
        trigger: TriggerT,
        invocation_policy: ENUMS.invocation_policy
        = ENUMS.invocation_policy.ONCE_PER_LOOP,
    ):
        """Alias for decorator_register."""
        return self.decorator_register(trigger, invocation_policy)

    @property
    def registered_triggers(self):
        yield from self.registered_actions.keys()

    @property
    def registered_events_actions(self):
        yield from self.registered_actions.values()

    def __iter__(self):
        yield from self.registered_actions.items()


class OptionsEnabledList():
    """
    TODO make events (callables) that can be executed on each frame 
    (or variable frame) 
    ex: every 1 frame or 10 frames
    (with or without an option required) option: variable that simulates configs for the game engine
    ex: if Game.Options.Stepped_Frames=ON > every {variable; mentioned above} frame wait until keyboard.get_pressed("Enter") 
    ! not each pause should the engine fix movements from delta time or else things would teleport far ahead
        ? check elapsed time and subtract from the dt to get accurate measures
    """
    ...


class EventsQueue[ContextT, R= Any]:
    __slots__ = "before", "after"

    def __init__(self) -> None:
        self.before: Callbacks[ContextT, R] = Callbacks[ContextT, R]()
        self.after: Callbacks[ContextT, R] = Callbacks[ContextT, R]()


class StateEvents:
    __slots__ = ("draw_events_Queue", "update_events_Queue",
                 "on_enter", "on_leave", "on_destroy", "on_create")

    def __init__(self) -> None:
        self.draw_events_Queue = EventsQueue[DrawEventContext]()
        self.update_events_Queue = EventsQueue[StateEventContext[None]]()

        self.on_enter = Callbacks[StateEventContext[None]]()
        self.on_leave = Callbacks[StateEventContext[None]]()
        self.on_create = Callbacks[StateEventContext[None]]()
        self.on_destroy = Callbacks[StateEventContext[None]]()


class KeyboardEvents:
    def __init__(self) -> None:
        self.streamed = Callbacks[StateEventContext[pygame.key.ScancodeWrapper]]()
        self.pressed = Callbacks[StateEventContext[pygame.key.ScancodeWrapper]]()


class EventsHandler:
    def __init__(self) -> None:
        self.State_Events = StateEvents()
        self.Keyboard_Event = KeyboardEvents()
        self.Pygame_Event = EventsDict[int | ENUMS.TRIGGERS, pygame.event.Event]()
