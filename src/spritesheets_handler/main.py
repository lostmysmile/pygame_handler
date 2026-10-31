from spritesheets_handler.helper import cooldown


from pathlib import Path
from collections.abc import Generator, Iterable
from typing import Any, NamedTuple,  Tuple, Union, cast
import pygame

dir_path = Path(__file__).parent

Coordinate = pygame.Vector2


class Size[T:int | float= int](NamedTuple):
    width: T = cast(T, 0)
    height: T = cast(T, 0)

    @classmethod
    def create(cls, tuple: Tuple[T, T]):
        return cls(*tuple)


class Shape (NamedTuple):
    columns: int
    rows: int


type Coord = Union["Coordinate", Tuple[int, int], pygame.Rect]


def normalize_dest(dest: Coord) -> Union[Tuple[int, int], pygame.Rect]:
    if isinstance(dest, (tuple, pygame.Rect)):
        return dest
    return (int(dest.x), int(dest.y))


def load_image(path: str | Path) -> pygame.Surface:
    return pygame.image.load(path)


class sprite_instance:
    def __init__(self, image: pygame.Surface):
        self.image = image
        self.size = Size.create(image.size)

    def get_convert_alpha(self):
        return self.image.convert_alpha()

    def get_convert(self):
        return self.image.convert()

    def optimize_transparent(self):
        self.image = self.get_convert_alpha()

    def optimize(self):
        self.image = self.get_convert()


class sprites_sheet:
    def __init__(self, sheet_location: str, rows: int, columns: int):
        self.Sprites: list[sprite_instance] = []

        self.Shape = Shape(columns, rows)

        self.SourceImage = load_image(dir_path/sheet_location)
        self.SourceImage_size = Size.create(self.SourceImage.size)

        self._load_sprites()

    def _load_sprites(self):
        self.Sprites.clear()

        width, height = self.SourceImage_size
        rows, columns = self.Shape
        sub_sprite_width, sub_sprite_height = width//rows, height//columns

        # * Calculate each sprite offset and append to sprites list
        for x in range(columns):
            for y in range(rows):
                offset_x = sub_sprite_width*y
                offset_y = sub_sprite_height*x

                sprite_rect = (
                    (offset_x, offset_y), (sub_sprite_width, sub_sprite_height))

                sprite_image = self.SourceImage.subsurface(sprite_rect)

                sprite_object = sprite_instance(sprite_image)

                self.Sprites.append(sprite_object)

    def __iter__(self) -> Generator[sprite_instance, Any, None]:
        yield from self.Sprites

    def __len__(self) -> int:
        return len(self.Sprites)

    def __getitem__(self, index: int) -> sprite_instance:
        return self.Sprites[index]

    def __setitem__(self, index: int, item: sprite_instance):
        self.Sprites[index] = item

    def __delitem__(self, i: slice):
        del self.Sprites[i]

    def optimize(self, isTransparent: bool = False):
        for sprite in self.Sprites:
            if isTransparent:
                sprite.optimize_transparent()
            else:
                sprite.optimize()


class index_slice_handler:
    """_`active` is the actual index while `relative` starts from 0_
    """

    def __init__(self, start: int, end: int) -> None:
        self.start = self.active = start
        self.end = end

    def __str__(self) -> str:
        return f"{self.active}"

    def reset(self) -> int:
        self.active = self.start
        return self.active

    def increment(self, amount: int = 1) -> int:
        self.active += amount
        if self.active >= self.end:
            self.reset()
        return self.active

    @property
    def relative(self) -> int:
        """index count from start to end (starts from 0)"""
        return self.active-self.start

    @property
    def range_Slice(self):
        return slice(self.start, self.end)


class animation_handler:
    display_next_animation = False
    """_skips current sprite if set to true_"""

    def __init__(self, sprites_sheet: sprites_sheet, IndexOfFirstSprite: int = 0, IndexOfLastSprite: int|None = None):
        IndexOfLastSprite = IndexOfLastSprite if IndexOfLastSprite is not None else len(
            sprites_sheet.Sprites)

        self.sprites_sheet = sprites_sheet

        self.index = index_slice_handler(IndexOfFirstSprite, IndexOfLastSprite)

    def __iter__(self) -> Generator[sprite_instance, Any, None]:
        yield from self.sprites_sheet

    def __len__(self) -> int:
        return len(self.sprites_sheet)

    @property
    def available_sprites(self):
        """Returns selected sprites from active 'sprites_sheet'"""
        return self.sprites_sheet.Sprites[self.index.range_Slice]

    @property
    def current_sprite(self):
        return self.sprites_sheet[self.index.active]

    def next_sprite(self):
        return self.sprites_sheet[self.index.increment()]

    def __next__(self):
        return self.next_sprite()

    def draw_onto(self, surface: pygame.Surface, dest: Coord, disable_skipping_Anim: bool = True):
        if (self.display_next_animation):
            (self.next_sprite())

        img = self.current_sprite.image

        surface.blit(img, normalize_dest(dest))

        if disable_skipping_Anim:
            self.display_next_animation = False


class automatic_timed_animation_handler_for(animation_handler):
    def __init__(self, sprites_sheet: sprites_sheet, IndexOfFirstSprite: int = 0, IndexOfLastSprite: int | None = None, interval: float = 0):
        super().__init__(sprites_sheet, IndexOfFirstSprite, IndexOfLastSprite)
        self.timer = cooldown(interval)
        self.auto_increment = self.timer.assign_cooldown(self.index.increment)

    def draw_onto(self, surface: pygame.Surface, dest: Coord, disable_skipping_Anim: bool = True):
        # if self.timer.has_passed():
        #     self.index.increment()
        
        self.auto_increment()
        return super().draw_onto(surface, dest, disable_skipping_Anim)
        


# file = load_sprite_image("spritesheet.png")
# test = load_sprite_image("spritesheet.png")
# file = load_sprite_image("sheet.jpg")

if __name__ == '__main__':
    def show_sprites(offset: tuple[int, int], sprites: Iterable[sprite_instance]):
        x, y = offset
        for image in sprites:
            if x + image.size .width > screen.width:
                y += image.size.height
                x = offset[0]
            screen.blit(image.image, (x, y))
            x += (image.size.width)

    def test_spritesSheet():
        global running
        active = running
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
            screen.fill((0, 0, 0))
            show_sprites((0, 0), test.Sprites)

            pygame.display.flip()
        running = active

    def test_animation():
        global running
        active = running
        while active:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run_anim.display_next_animation = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    run_anim.display_next_animation = False

                elif event.type == pygame.QUIT:
                    active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run_anim.display_next_animation = True

            screen.fill((0, 0, 0))
            show_sprites((100, 500), run_anim)

            run_anim.draw_onto(screen, (0, 0))

            pygame.display.flip()
        running = active

    def test_autoAnimation():
        global running
        active = running
        while active:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    active = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        auto_run_anim.display_next_animation = True

            screen.fill("white")
            show_sprites((50, 90), test.Sprites)
            show_sprites((50, 500), auto_run_anim)
        
            auto_run_anim.draw_onto(screen, (0, 0))

            pygame.display.flip()
        running = active

    pygame.init()
    # test = sprites_sheet("testing/test.jpg", 2, 6)
    # test = sprites_sheet("testing/test2.jpg", 2, 6)
    test = sprites_sheet("testing/spritesheet.png", 6, 2)
    # test.optimize(isTransparent=True)
    # test = sprites_sheet("testing/sheet-resized.jpg", 1, 4)
    # run_anim = animation(test, 3, 5)
    # run_anim = animation(test, cooldown=.05)
    # run_anim = animation(test, 1, 9)
    # auto_run_anim = automatic_timed_animation(test, 1, 9, timer=.1)
    run_anim = animation_handler(test)
    auto_run_anim = automatic_timed_animation_handler_for(
        test, interval=1.5)

    FONT = pygame.font.SysFont("sans", size=30)
    for idx, sprite in enumerate(test.Sprites):
        text = FONT.render(f"{idx}", False, "red")
        sprite.image.blit(text)

    screen = pygame.display.set_mode((500, 500), flags=pygame.RESIZABLE)
    running = True
    test_spritesSheet()
    running = True
    test_animation()
    running = True
    test_autoAnimation()
