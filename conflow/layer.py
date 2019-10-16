from abc import abstractmethod
from typing import TypeVar, Union, Optional

from conflow.manager import Config
from conflow.merge import merge_factory
from conflow.node import node_factory, TU
from typing_extensions import Protocol

T = TypeVar('T')
TK = Union[str, int]


class LayerProtocol(Protocol):
    """Layer interface describes base Layer methods."""

    @abstractmethod
    def __init__(self,
                 config: Config,
                 settings: T,
                 name: Optional[TK] = None
                 ) -> None: ...

    @abstractmethod
    def tree(self) -> TU: ...

    @abstractmethod
    def merge(self, other: 'LayerProtocol') -> None: ...


class Layer(LayerProtocol):
    """
    Layer class is a settings item, for example settings from `.yml` file,
    `.env` file or pure Python dictionary.

    Provide an interface for merge settings items.
    """
    def __init__(self,
                 config: Config,
                 settings: T,
                 name: Optional[TK] = None
                 ) -> None:
        self.config = config
        self.__name: TK = name if name is not None else id(self)
        self.__tree = node_factory(self.__name, settings)

    def tree(self) -> TU:
        return self.__tree

    def merge(self, other: LayerProtocol) -> None:
        """Implement merge functionality."""
        self.__tree = merge_factory(self.tree(), other.tree(), self.config)
