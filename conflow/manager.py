from typing import Callable, TypeVar, Union, MutableMapping, cast, Optional
from typing import Any

import conflow
from conflow.node import AbstractNode, Node, NodeList, NodeMap, TV as NB
from conflow.policy import (
    MergeDifferentTypesPolicy,
    NotifyDifferentTypesPolicy,
    MergeListPolicy,
)

TK = Union[str, int]
T = TypeVar('T')
TP = TypeVar('TP')

#  NB = TypeVar('NB', int, float, str, bool, None)
TB = TypeVar('TB', bound=AbstractNode)
TO = TypeVar('TO', bound=AbstractNode)
NO = TypeVar('NO', int, float, str, bool, None)
TR = Union[
    Node[NO],
    NodeList[TO],
    NodeMap[TO],
    NodeList[Union[TB, TO]],
    NodeMap[Union[TB, NO]],
    NodeMap[Union[TB, TO]],
]

T_BASE = Union[Node[NB], NodeList[TB], NodeMap[TB]]
T_OTHER = Union[Node[NO], NodeList[TO], NodeMap[TO]]
#  T_MERGE_FUNC = Callable[[T_BASE[NB, TB],
                         #  T_OTHER[NO, TO]],
                        #  TR[NO, TO, TB]]
T_MERGE_FUNC = Callable[..., TR[NO, TO, TB]]


def merge(_: TB, other: TO) -> AbstractNode[TO]:
    return other


class Config:
    """
    Config is a manager class provided an interface for the creation
    and merging Layers from different sources.
    """

    def __init__(self,
                 merge_different: Optional[Callable] = None,
                 #  MergeDifferentTypesPolicy.not_strict,
                 merge_list: Callable[[T, TP], TP] =
                 MergeListPolicy.override,
                 notification: Callable[..., None] =
                 NotifyDifferentTypesPolicy.warning,
                 ) -> None:
        if merge_different is None:
            self.merge_different: Callable = merge
        else:
            self.merge_different = merge_different
        self.merge_list = merge_different
        self.notification = merge_different
        self.layer: conflow.LayerProtocol = conflow.Layer(
            cast('conflow.Config', self), {})

    def merge(self, settings: MutableMapping[TK, T]) -> 'Config':
        """
        Merges two layers
        :param settings: source dictionary
        """
        layer = conflow.Layer(cast('conflow.Config', self), settings)
        self.layer.merge(layer)
        return self

    def __getitem__(self, key: TK) -> AbstractNode[T]:
        """
        Implementation of __getitem__ magic method.

        :param key: Access key for data
        """
        return self.layer.tree()[key]

    def __getattr__(self, name: TK) -> AbstractNode[T]:
        """
        Implementation of __getattr__ magic method.

        :param name: Attribute name (data access key)
        """
        return self.layer.tree().get(name)
