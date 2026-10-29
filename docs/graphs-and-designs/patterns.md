# Design Patterns

The project contains several recognizable design patterns or pattern-like structures. Some are deliberate, while others are useful descriptions of the code as it exists today. This is not a claim that every pattern is fully implemented or follows a canonical GoF definition.

## 1. Callback registry / Observer-style event handling

**Where:** `scene/events/events.py` — `EventsDict`, `Callbacks`, and `EventsHandler`.

Code registers a callable against one or more triggers. When matching input is dispatched, the registered callable receives an event context. Global registrations and scene-local registrations are combined by the scene dispatcher.

**Why it helps:** game systems can respond to events without forcing the central loop to know every gameplay action.

**Current limitation:** dispatch behavior and invocation policies need more tests. The current `ONCE_PER_LOOP` behavior is scoped to a batch of Pygame events, and the other policies are not fully distinct in the dispatcher.

## 2. Scene / state-transition model

**Where:** `scene/Scene.py` — `Scene` and `Scenes_handler`.

The handler tracks an active scene, a previous scene, and queued scenes. Scene transitions call `on_leave()` and `on_enter()` hooks.

**Why it helps:** separates different parts or modes of a game so each scene can own its entities and local callbacks.

**Terminology note:** this resembles a state pattern and a scene manager. It is not a complete finite-state-machine framework, and callers should follow the actual queue and transition behavior rather than assume a conventional stack.

## 3. Application controller / Facade-like coordinator

**Where:** `system/core.py` — `Game`.

The `Game` object brings together the window, scene handler, input polling, updates, and drawing sequence.

**Why it helps:** the top-level application has one place to start and run the game.

**Boundary:** `Game` still performs several responsibilities. As the project grows, extracting input polling or frame orchestration may make unit testing easier, but this should be driven by concrete complexity rather than abstraction for its own sake.

## 4. Composition

**Where:** `Scene`, `Game`, and `Window`.

A scene owns its local `EntitiesHandler` and `EventsHandler`; the game owns its scene handler and window; the window owns its clock and optional background.

**Why it helps:** behavior can be assembled from smaller collaborators rather than requiring a deep inheritance tree.

**Boundary:** the class-level `Scenes_handler.Global_Events` registry is shared state. Tests and applications that need independent game instances should account for this and clear or isolate registrations where appropriate.

## 5. Decorator-based registration

**Where:** `EventsDict.decorator_register()` and its `register_decorator()` alias.

The methods return a decorator which registers a function when it is defined.

Example:

```python
import pygame
from pygame_handler.scene.Scene import Scenes_handler
from pygame_handler.scene.events import StateEventContext

@Scenes_handler.Global_Events.Pygame_Event.decorator_register(pygame.QUIT)
def on_quit(context: StateEventContext):
    context.active_state.running = False
```

This style is convenient for fixed registrations near the callback definition. Use explicit `.register(...)` calls when registration needs to happen conditionally or at runtime.

## 6. Context object / parameter object

**Where:** `StateEventContext` and `DrawEventContext`.

Instead of passing several unrelated arguments to every callback, the dispatcher packages relevant information into a context object. The state-event context currently carries the active scene, an optional triggered event, and optional delta time. The draw context carries the active scene.

**Why it helps:** callback signatures stay consistent within a dispatcher, and additional context can be added centrally.

**Boundary:** different dispatcher families have different contexts. A callback intended for a draw event should not assume it receives a `StateEventContext`.

## 7. Delta-time-driven update

**Where:** `graphics/main.py` — `clock_handler`; `system/core.py`; `movement/main.py`.

The clock converts the frame duration from milliseconds to seconds and exposes it as `dt`. Movement helpers use elapsed time when calculating movement amounts.

**Why it helps:** movement calculations can depend on elapsed time rather than assuming a fixed frame rate.

**Boundary:** delta time alone does not provide collision detection, fixed-step simulation, or physics integration; those are separate concerns.

## Patterns not yet to rely on

- **Strategy for invocation policy:** the policy enum exists, but the dispatcher does not yet implement clearly separated behavior for every value. Treat this as an incomplete design direction, not a finished Strategy implementation.
- **Complete event-bus abstraction:** the callback maps provide event-bus-like behavior, but lifecycle events, keyboard events, and Pygame events use different structures and contexts. Their behavior is not yet uniform.
- **Dependency injection:** several components construct their dependencies directly, and global event registrations are shared. This is a potential future improvement for isolation and testing, not an existing project-wide pattern.

## Testing advice

For each new pattern-like abstraction, test the externally observable behavior first. Examples include callback call counts for each invocation policy, scene enter/leave order, separation of global and scene-local registrations, and movement calculations at different `dt` values.
