from .env import load_debug_configs as loadenv
from .ini import load_debug_configs as loadini

__all__ = "loadini","loadenv"