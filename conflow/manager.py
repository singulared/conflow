from typing import Callable, TypeVar, Union, Dict

import conflow
from conflow.node import AbstractNode
from conflow.policy import (
    MergeDifferentTypesPolicy,
    NotifyDifferentTypesPolicy,
    MergeListPolicy
)

TK = Union[str, int]
T = TypeVar('T')
TP = TypeVar('TP')


class Config:
    """
    Config is a manager class provided an interface for the creation
    and merging Layers from different sources.
    """

    def __init__(self,
                 merge_different: Callable[[AbstractNode, AbstractNode],
                                           AbstractNode] =
                 MergeDifferentTypesPolicy.not_strict,
                 merge_list: Callable[[AbstractNode, AbstractNode],
                                      AbstractNode] =
                 MergeListPolicy.override,
                 notification: Callable[..., None] =
                 NotifyDifferentTypesPolicy.warning,
                 ) -> None:
        self.merge_different = merge_different
        self.merge_list = merge_list
        self.notification = notification
        self.layer: conflow.LayerProtocol = conflow.Layer(
            self, {})  # type: ignore

    def merge(self, settings: Dict[str, T]) -> 'Config':
        """
        Merges two layers
        :param settings: source dictionary
        """
        layer = conflow.Layer(self, settings)  # type: ignore
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
        if isinstance(name, str):
            return getattr(self.layer.tree(), name)
        else:
            raise ValueError("Attribute must be str only")
