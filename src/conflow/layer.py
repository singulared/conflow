from abc import abstractmethod
from typing import TypeVar, Union, Optional

from conflow.merge import merge_factory
from conflow.node import node_factory, TU
from conflow.policy import MergePolicy
from typing_extensions import Protocol

T = TypeVar('T')
TK = Union[str, int]


class LayerProtocol(Protocol):
    """Layer interface describes base Layer methods."""
    @abstractmethod
    def tree(self) -> TU: ...

    @abstractmethod
    def merge(self,
              other: 'LayerProtocol',
              policy: MergePolicy = MergePolicy.EXTEND
              ) -> None: ...


class Layer(LayerProtocol):
    """
    Layer class is a settings item, for example settings from `.yml` file,
    `.env` file or pure Python dictionary.

    Provide an interface for merge settings items.
    """
    def __init__(self,
                 settings: T,
                 name: Optional[TK] = None
                 ) -> None:
        self.__name: TK = name if name is not None else id(self)
        self.__tree = node_factory(self.__name, settings)

    def tree(self) -> TU:
        return self.__tree

    def merge(self,
              other: LayerProtocol,
              policy: MergePolicy = MergePolicy.EXTEND
              ) -> None:
        """Implement merge functionality."""
        self.__tree = merge_factory(self.tree(), other.tree(), policy)
