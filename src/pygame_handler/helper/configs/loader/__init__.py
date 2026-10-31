from .env import load_configs as loadenv
from .ini import load_configs as loadini

__all__ = "loadini","loadenv"