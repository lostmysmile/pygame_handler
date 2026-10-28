from typing import Literal

class NO_TRIGGERS:
    __slots__ = ()
    type TYPE = Literal["{NONE}"]
    VALUE: Literal["{NONE}"]= "{NONE}"

class ALL_TRIGGERS:
    __slots__ = ()
    type TYPE = Literal["{ALL}"]
    VALUE:Literal["{ALL}"] = "{ALL}"
