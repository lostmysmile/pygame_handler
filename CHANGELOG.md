# Changelog

This file tracks notable changes in the repository's development history. The project is actively developed, and this log does not imply that a version has been published unless a release is explicitly announced.

## Unreleased

### Added

- Added an MIT license and declared the license and project metadata in `pyproject.toml`.
- Added a `src/pygame_handler/` package layout for the library modules.
- Added event callback registration for one trigger or multiple triggers, callback validation, invocation-policy metadata, and focused pytest coverage for event behavior.
- Centralized debug flags and environment-based configuration, including support for individual settings and an `ALL` fallback.
- Added helper scripts for starting the game, running tests, creating a virtual environment, and activating it from Windows CMD, PowerShell, and Git Bash.
- Added separate optional dependency groups for standard Pygame, Pygame CE, and tests.

### Changed

- Reorganized the runtime around `pygame_handler.system.core.Game` and scene handling in `pygame_handler.scene`.
- Renamed the earlier state-handling concepts to scenes and moved graphics, movement, logging, and debugging helpers into the package namespace.
- Set the declared minimum Python version to 3.15.
- Updated the README to use the current package entry point and repository scripts.

### Fixed

- Added explicit validation so event registration rejects non-callable callbacks and invalid trigger inputs with errors.
- Made environment-option matching case-insensitive.
- Updated the launch and test scripts to use the current package path and consistent pytest options.

### Known gaps

- The event invocation policies are not yet fully implemented or tested as distinct behaviors.
- The spritesheets package still has import/export and dependency issues; see [the spritesheets README](src/pygame_handler/spritesheets/README.md).
- Automated test coverage remains narrow, and CI currently runs on Ubuntu rather than testing the Windows helper scripts.
