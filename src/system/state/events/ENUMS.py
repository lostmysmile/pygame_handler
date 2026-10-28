from enum import Enum, StrEnum, auto
from typing import Literal


class invocation_policy(Enum):
    EVERY_TIME = auto()
    ONCE_PER_LOOP = auto()
    ONCE_PER_EVENT = auto()


class TRIGGERS(StrEnum):
    NONE = "{NONE}"
    ALL = "{ALL}"


class NO_TRIGGERS:
    __slots__ = ()
    type TYPE = Literal["{NONE}"]
    VALUE: Literal["{NONE}"] = "{NONE}"


class ALL_TRIGGERS:
    __slots__ = ()
    type TYPE = Literal["{ALL}"]
    VALUE: Literal["{ALL}"] = "{ALL}"
