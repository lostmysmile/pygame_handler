
from enum import Enum, StrEnum, auto


class invocation_policy(Enum):
    EVERY_TIME = auto()
    ONCE_PER_LOOP = auto()
    ONCE_PER_EVENT = auto()


class TRIGGERS(StrEnum):
    NONE = "{NONE}"
    ALL = "{ALL}"
