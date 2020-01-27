import logging
from typing import Union, TypeVar, Any

from conflow.node import NodeList, Node, NodeMap

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
    def strict(_: T, other: TP) -> TP:
        return other

    @staticmethod
    def not_strict(base: T, other: TP) -> None:
        raise RuntimeError(
            'Cannot merge mismatched types {base} {other}.'.format(
                base=type(base).__name__,
                other=type(other).__name__
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
    extend option is used to add other values ​​to the base.
    """

    @staticmethod
    def override(_: T, other: TP) -> TP:
        return other

    @staticmethod
    def extend(base: NodeList[T], other: NodeList[TP]
               ) -> NodeList[Union[T, TP]]:
        return NodeList(base._key, [*base, *other])
