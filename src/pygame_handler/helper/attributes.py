
from typing import Any


def attrsetter(obj:object,attribute:str,value:Any):
    """
    attrsetter _Sets nested attributes to object_

    Args:
        obj (object)
        attribute (str): _you can use dot notation_
        value (Any): 

    Raises:
        ValueError: _attribute argument is empty or an empty string_
        ValueError: _Incorrect use of dot notation_

    Examples:
        >>> class Nested:
        ...     class Target:
        ...         x = None
        >>> attrsetter(Nested,"Target.x",1)
        >>> print(Nested.Target.x) # 1
        1
    """
    if not attribute:
        raise ValueError("Attribute cannot be empty")    

    parts = attribute.split(".")

    if not all(parts):
        raise ValueError(f"Invalid attribute path: {attribute!r}")

    *parent_attrs,last_attr = parts

    for parent_attr in parent_attrs:
        obj = getattr(obj,parent_attr)
    
    setattr(obj,last_attr,value)