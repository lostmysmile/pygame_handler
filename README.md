# pygame_handler

A Python helper library for building game loops with [Pygame](https://www.pygame.org/).

## Requirements

- Python 3.15 or newer.
- Choose **one** Pygame implementation: `pygame` or `pygame-ce`. The examples below use `pygame-ce`.

## Install from source

Run these commands from the repository root:

```console
git clone https://github.com/lostmysmile/pygame_handler.git
cd pygame_handler
python -m venv .venv
```

Activate the environment in your terminal:

**Windows CMD**
```bat
.venv\Scripts\activate.bat
```

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Git Bash on Windows**
```bash
source .venv/Scripts/activate
```

Install the project with Pygame CE:

```console
python -m pip install -e ".[pygame-ce]"
```

To use the standard Pygame package instead, install `.[pygame]` instead of `.[pygame-ce]`. Do not install both extras into the same environment.

To install the test dependencies as well:

```console
python -m pip install -e ".[test,pygame-ce]"
```

## Run the example game

Run commands from the repository root with the virtual environment activated.

On Windows, use the repository's [`scripts/run.bat`](scripts/run.bat):

**CMD**
```bat
scripts\run.bat
```

**PowerShell**
```powershell
.\scripts\run.bat
```

The batch file launches the same Python module used by the direct command below. In any terminal, you can run it directly:

```console
python -m pygame_handler.system.core
```

## Run the tests

Install the test extra first, then run:

```console
python -m pytest -ra --strict-config --strict-markers
```

On Windows, you can use [`scripts/test.bat`](scripts/test.bat) instead:

```bat
scripts\test.bat
```

## Project layout

- `src/pygame_handler/` — library source code.
- `tests/` — automated tests.
- `scripts/` — Windows run/test helpers and virtual-environment scripts.
- `pyproject.toml` — package metadata and dependencies.

## Documentation

- [Architecture overview](ARCHITECTURE.MD) — runtime flow, package responsibilities, and known limitations.
- [Changelog](CHANGELOG.md) — notable changes in the current development line.
- [Spritesheet helper notes](src/pygame_handler/spritesheets/README.md) — experimental module status and known import blockers.
- [Graphs, designs, and patterns](docs/graphs-and-designs/README.md) — Mermaid diagrams, component design, and pattern notes.

## License

pygame_handler is licensed under the MIT License. See [`LICENSE`](LICENSE) for the full text.
