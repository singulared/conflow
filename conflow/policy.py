import logging
from typing import Union, TypeVar, Any, cast, Optional
from itertools import chain

from conflow.node import NodeList, Node, NodeMap, AbstractNode

logger = logging.getLogger(__name__)

T = TypeVar('T')
TP = TypeVar('TP')
TT = TypeVar('TT')
TU = Union[Node[Any], NodeList[Any], NodeMap[Any]]


class MergeDifferentTypesPolicy:
    """
    The class describes the behavior when merged different types of nodes.

    `strict` raise an exception if different types are merged.
    `not_strict` return `other` node.
    """
    @staticmethod
    def not_strict(_: AbstractNode, other: AbstractNode) -> AbstractNode:
        return other

    @staticmethod
    def strict(base: AbstractNode, other: AbstractNode) -> None:
        raise RuntimeError(
            'Cannot merge `{base_key}` and `{other_key}` with key `{key}`'.format(
                base_key=base(),
                other_key=other(),
                key=base._key
            )
        )


class NotifyDifferentTypesPolicy:
    """
    The class describes the behavior when merged different types of nodes.

    `warning` logged with warning level.
    `quiet` do nothing.
    """

    @staticmethod
    def warning(base: T, other: TP) -> None:
        logger.warning('Merge different types %s : %s', base, other)

    @staticmethod
    def quiet(base: T, other: TP) -> None:
        ...


class MergeListPolicy:
    """
    Class describes list merge policies.

    override option is used to replace the base value with another value.
    extend option is used to add other values to the base.
    """

    @staticmethod
    def override(_: AbstractNode, other: AbstractNode) -> AbstractNode:
        return other

    @staticmethod
    def extend(base: NodeList[T], other: NodeList[TP]
               ) -> NodeList[Optional[Union[T, TP]]]:
        return NodeList(
            base._key,
            [cast(AbstractNode[Union[T, TP]], node)() for node in chain(
                base, other)])
