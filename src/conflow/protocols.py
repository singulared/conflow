import typing
from typing import Any
from typing_extensions import Protocol
from abc import abstractmethod

CT = typing.TypeVar("CT", bound="Comparable")


class Comparable(Protocol):
    @abstractmethod
    def __eq__(self, other: Any) -> bool: ...

    @abstractmethod
    def __lt__(self: CT, other: CT) -> bool: ...

    def __gt__(self: CT, other: CT) -> bool:
        return (not self < other) and self != other

    def __le__(self: CT, other: CT) -> bool:
        return self < other or self == other

    def __ge__(self: CT, other: CT) -> bool:
        return (not self < other)
