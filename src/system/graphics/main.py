from typing import TYPE_CHECKING, Union

import pygame
from pathlib import Path

if TYPE_CHECKING:
    from ..state.State import State

class Background:
    def __init__(self, color: str | None = None, image: str | None = None) -> None:
        self.color = color
        self.image = image
        # TODO add image handler
        if self.image:
            self.image_surf = pygame.image.load(self.image)
        else:
            self.image_surf = None

    def update(self):
        pass  # Placeholder for animation or updates

    def draw_on(self, surf: pygame.Surface):
        if self.color is not None:
            surf.fill(self.color)

        if self.image_surf:
            surf.blit(self.image_surf, (0, 0))


class Graphics_object:
    def __init__(self, size=(50, 50)) -> None:
        self.image = pygame.Surface(size)

    def update(self):
        ...

    def draw_on(self, surf: pygame.Surface, dest):
        surf.blit(self.image, dest)


class Default_Entity_object:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y
        self.graphics = Graphics_object()

    def update(self):
        self.graphics.update()

    def draw_on(self, surf: pygame.Surface):
        self.graphics.draw_on(surf, self.pos)

    @property
    def pos(self):
        return self.x, self.y


class EntitiesHandler:
    def __init__(self, l: list | None = None) -> None:
        self.entity_list: list[Default_Entity_object] = []

    def update_and_drawOn(self, surf: pygame.Surface):
        for entity in self.entity_list:
            entity.update()
            entity.draw_on(surf)

    def update(self):
        for entity in self.entity_list:
            entity.update()

    def draw_on(self, surf: pygame.Surface):
        for entity in self.entity_list:
            entity.draw_on(surf)

    def __iter__(self):
        yield from self.entity_list

class clock_handler:
    def __init__(self, fps_target: float = 60) -> None:
        self.fps_target: float = fps_target

        self.dt: float = 0
        self.time_since_last_frame: int = 0

        self.pygame_clock = pygame.time.Clock()

    def tick(self) -> int:
        """Returns time since last frame in milliseconds"""
        self.time_since_last_frame = self.pygame_clock.tick(self.fps_target)
        self.dt = self.time_since_last_frame / 1000.0
        return self.time_since_last_frame


cur_dir = Path(__file__).parent
icon_location = cur_dir/"quality_icon2.png"
default_icon = pygame.image.load(icon_location.as_posix(), "Game_Icon")


class Window:
    def __init__(self, name: str = "Window", background_handler: Background | None = None, size: tuple[int, int] = (0, 0), fps_target: float = 60) -> None:
        pygame.init()  # Initialize pygame
        self.name: str = name
        self.background = background_handler
        self.clock = clock_handler(fps_target=fps_target)
        self.screen = pygame.display.set_mode(size=size)
        pygame.display.set_caption(name, "icon_title LOL")

        pygame.display.set_icon(default_icon)

    def update(self):
        if self.background:
            self.background.update()

    def draw(self, state: Union[State, None] = None) -> None:
        if self.background:
            self.background.draw_on(self.screen)
        if state:
            state.draw_on(self.screen)
        pygame.display.flip()


if __name__ == '__main__':

    def main():
        bg = Background("white")
        window = Window(background_handler=bg, size=(500, 500))
        states = States()
        running = True
        while running:
            window.clock.tick()   # Delta time in seconds
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            # for event in events:
            #     if event.type == pygame.QUIT:
            #         running = False
            if __debug__:
                continue
            if states.active_state:
                states.active_state.handle_pygame_events(events)
                states.active_state.handle_keyboard_input(keys)
                states.active_state.update(window.clock.dt)
            window.draw(states.active_state)
        pygame.quit()

    main()
