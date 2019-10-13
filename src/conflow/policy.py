from enum import Enum


class MergePolicy(Enum):
    """
    Class describes merge policies.

    OVERRIDE option is used to replace the base value with another value.
    EXTEND option is used to add other values ​​to the base.
    """
    OVERRIDE = 0
    EXTEND = 1
