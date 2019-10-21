import logging
from enum import Enum

from typing import Union, TypeVar, Any

from conflow.node import NodeList, Node, NodeMap
from mypy_extensions import NoReturn

logger = logging.getLogger(__name__)

T = TypeVar('T')
TP = TypeVar('TP')
TT = TypeVar('TT')
TU = Union[Node[Any], NodeList[Any], NodeMap[Any]]


def return_other(_: T, other: TP) -> TP:
    return other


def raise_error(base: T, other: TP) -> NoReturn:
    raise RuntimeError('Cannot merge mismatched types {base} {other}.'.format(
        base=type(base).__name__,
        other=type(other).__name__
    ))


class MergeDifferentTypesPolicy(Enum):
    """
    The class describes the behavior when merged different types of nodes.

    STRICT raise an exception if different types are merged.
    NOT_STRICT return `other` node.
    """
    STRICT = raise_error
    NOT_STRICT = return_other


def notify_warning(base: T, other: TP) -> None:
    logger.warning('Merge different types %s : %s', base, other)


def quiet(base: T, other: TP) -> None:
    ...


class NotifyDifferentTypesPolicy(Enum):
    """
    The class describes the behavior when merged different types of nodes.

    WARNING logged with warning level.
    QUIET do nothing.
    """
    WARNING = notify_warning
    QUIET = quiet


def override_nodelist(_: T, other: TP) -> TP:
    return other


def extend_nodelist(base: NodeList[T], other: NodeList[TP]
                    ) -> NodeList[Union[T, TP]]:
    return NodeList(base._key, [*base, *other])


class MergeListPolicy(Enum):
    """
    Class describes list merge policies.

    OVERRIDE option is used to replace the base value with another value.
    EXTEND option is used to add other values ​​to the base.
    """
    OVERRIDE = override_nodelist
    EXTEND = extend_nodelist
