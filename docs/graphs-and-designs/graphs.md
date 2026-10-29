# Graphs

These diagrams are based on the current source in `src/pygame_handler/`. They are intended to help readers trace the flow of control before reading individual modules.

## 1. Main game-loop flow

`Game.game_loop()` initializes the active scene, then repeats frame timing, input dispatch, updates, and drawing while the active scene's `running` flag is true.

```mermaid
flowchart TD
    A["Game.game_loop()"] --> B["setUp(): activate initial scene"]
    B --> C{"active_scene.running?"}
    C -- No --> Z["Display goodbye notification"]
    C -- Yes --> D["clock.tick(): calculate dt"]
    D --> E["Collect events + keyboard state"]
    E --> F["Dispatch keyboard input"]
    F --> G["Dispatch Pygame events"]
    G --> H["Scene.update(dt)"]
    H --> I["Run update-before callbacks"]
    I --> J["Update entities"]
    J --> K["Run update-after callbacks"]
    K --> L["Update window/background"]
    L --> M["Draw background and scene"]
    M --> N["Run draw callbacks and draw entities"]
    N --> O["Flip display"]
    O --> P{"RUN_ONCE enabled?"}
    P -- Yes --> Z
    P -- No --> C
```

**Important:** this loop describes the current ordering. In particular, keyboard dispatch occurs before Pygame-event dispatch, and the scene's update and draw phases are separate.

## 2. Component relationship graph

```mermaid
classDiagram
    class Game {
      +States: Scenes_handler
      +window: Window
      +game_loop()
      +run_logic(scene)
      +update(scene)
      +draw(scene)
    }
    class Scenes_handler {
      +active_state: Scene
      +prev_state: Scene
      +deque
      +Global_Events
      +activate_next_state()
      +activate_previous_state()
    }
    class Scene {
      +running: bool
      +entities: EntitiesHandler
      +events_handler: EventsHandler
      +handle_keyboard_input()
      +handle_pygame_events()
      +update(dt)
      +draw_on(surface)
      +on_enter()
      +on_leave()
    }
    class Window {
      +screen
      +clock: clock_handler
      +background
      +update()
      +draw(scene)
    }
    class EventsHandler {
      +Pygame_Event: EventsDict
      +Keyboard_Event
      +State_Events
    }
    class EventsDict {
      +register(trigger, callback, policy)
    }
    class Callbacks {
      +register(callback, policy)
      +_invoke_all(context)
    }
    class EntitiesHandler {
      +entity_list
      +update()
      +draw_on(surface)
    }
    Game --> Scenes_handler : coordinates scenes
    Game --> Window : owns display
    Scenes_handler o--> Scene : active / previous / queued
    Scenes_handler --> EventsHandler : shared class-level registry
    Scene *--> EventsHandler : scene-local callbacks
    Scene *--> EntitiesHandler : scene entities
    EventsHandler *--> EventsDict : Pygame event callbacks
    EventsDict *--> Callbacks : callback groups
    Window --> Scene : requests drawing
```

The line from `Scenes_handler` to `EventsHandler` represents the class-level `Global_Events` registry. It is shared across handler instances, unlike the local `events_handler` owned by each scene.

## 3. Pygame-event dispatch

The scene dispatcher combines the global and scene-local Pygame-event registries, checks the current event's specific trigger and the `TRIGGERS.ALL` trigger, then invokes the resulting callback registrations.

```mermaid
flowchart TD
    A["pygame.event.get()"] --> B["Scene.handle_pygame_events(events)"]
    B --> C["Combine global and scene-local registries"]
    C --> D["For each event"]
    D --> E["Look up TRIGGERS.ALL callbacks"]
    D --> F["Look up event.type callbacks"]
    E --> G["Combine callback registrations"]
    F --> G
    G --> H["Iterate matching registrations"]
    H --> I{"Policy is ONCE_PER_LOOP and already handled?"}
    I -- Yes --> J["Skip this invocation"]
    I -- No --> K["Call callback(context)"]
    K --> L{"More registrations?"}
    J --> L
    L -- Yes --> H
    L -- No --> M{"More events?"}
    M -- Yes --> D
    M -- No --> N["Return to game loop"]
```

### Dispatch caveats

- `ONCE_PER_LOOP` currently tracks a registration in a set while processing one batch of Pygame events. It is not a global once-per-frame guarantee across keyboard, update, draw, or other callback groups.
- `EVERY_TIME` and `ONCE_PER_EVENT` do not currently have separate branches in the Pygame-event dispatcher. Do not rely on them as distinct policies until their semantics are implemented and tested.
- Keyboard handling currently invokes the `pressed` registry for both the just-pressed and continuously held key states. The separate `streamed` registry exists but is not used by that method yet; this is a code issue to resolve, not intended behavior.
