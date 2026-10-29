# Spritesheet helpers

> **Status: experimental.** The current implementation describes sprite-sheet slicing and animation helpers, but the package is not yet safe to rely on from an application. The import/export issues below need to be fixed before the examples can be treated as runnable API documentation.

## Intended functionality

The implementation in `main.py` contains these components:

- **`sprites_sheet`** loads an image and creates a sequence of `sprite_instance` objects from a grid. The constructor takes a sheet path, row count, and column count. The source image path is currently resolved relative to the `spritesheets/` module directory unless an absolute path is supplied.
- **`sprite_instance`** wraps a `pygame.Surface`, records its size, and exposes surface-conversion helpers for opaque or alpha-enabled images.
- **`animation_handler`** selects a range of sprites and draws its current sprite to a target surface. Its index helper tracks the current position in that range.
- **`automatic_timed_animation_handler_for`** extends the animation handler with a cooldown-driven index increment.
- **`cooldown`** provides elapsed-time checks and a decorator-style wrapper that runs a callable only when its interval has passed.
- **`load_file`** resolves a filename relative to a supplied directory and asserts that the path exists.

These names reflect the current implementation, not a promise that the API is stable.

## Current import blockers

The following problems were found in the current source and should be fixed before publishing usage examples as working instructions:

1. **Export-name mismatch:** `spritesheets/__init__.py` imports lowercase `shape` and `size`, while `main.py` defines `Shape` and `Size`. As written, the package-level import cannot find those lowercase names.
2. **Incorrect helper import:** `spritesheets/main.py` uses `from helper import cooldown` instead of importing the sibling module through the package. This assumes a top-level module named `helper` exists.
3. **Undeclared dependency:** `spritesheets/helper.py` imports `keyboard`, but `keyboard` is not declared in `pyproject.toml`. The import is performed even when the interactive helper demo is not being used.
4. **Grid dimensions need tests:** the sprite width/height calculations use the row and column counts in a way that may be transposed for non-square sheets. Add tests for square and non-square grids before relying on extraction coordinates.

## Recommended repair order

1. Choose and consistently use the public names `Shape`/`Size` (or deliberately provide lowercase aliases) in `main.py` and `__init__.py`.
2. Change the helper import to a package-relative import.
3. Remove the top-level `keyboard` requirement from production imports if it is only needed by the standalone demo, or declare it as an appropriate optional dependency.
4. Add tests that verify the number, size, and order of extracted sprites for both square and non-square grids.
5. Add tests for animation index boundaries, cooldown timing, and calls to `draw_onto`.

Until those changes are made and tested, treat this module as work in progress rather than a supported part of the library.
