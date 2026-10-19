from system import main

# from contextlib import suppress
game = main.Game()
game.DEBUG_MODE=True
# with suppress(NotImplementedError):
game.run()