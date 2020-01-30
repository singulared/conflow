"""
Implements merge functionality for every type of Nodes.

base: Layer instance that will be extend or override.
other: Layer instance that will be use for extend or override base.
policy: Enum option that define extend ot override operations.
"""
from typing import overload, cast, TypeVar

from conflow.manager import Config
from conflow.node import Node, NodeList, NodeMap, TU, AbstractNode

NB = TypeVar('NB', str, int, float, bool, None)
NO = TypeVar('NO', str, int, float, bool, None)
TB = TypeVar('TB')
TO = TypeVar('TO')
TR = TypeVar('TR')

# Node
@overload
def merge_factory(base: Node[NB],
                  other: Node[NO],
                  config: Config,
                  ) -> Node[NB]:
    """Implements merge of Node and Node."""
    ...


@overload
def merge_factory(base: Node[NB],
                  other: NodeList[TB],
                  config: Config,
                  ) -> NodeList[TB]:
    """Implements merge of Node and NodeList."""
    ...


@overload
def merge_factory(base: Node[NB],
                  other: NodeMap[TB],
                  config: Config,
                  ) -> NodeMap[TO]:
    """Implements merge of Node and NodeMap."""
    ...


# NodeList
@overload
def merge_factory(base: NodeList[TB],
                  other: Node[NO],
                  config: Config,
                  ) -> Node[NO]:
    """Implements merge of NodeList and Node."""
    ...


@overload
def merge_factory(base: NodeList[TB],
                  other: NodeList[TO],
                  config: Config,
                  ) -> NodeList[TO]:
    """Implements merge of NodeList and NodeList."""
    ...


@overload
def merge_factory(base: NodeList[TB],
                  other: NodeMap[TO],
                  config: Config,
                  ) -> NodeMap[TO]:
    """Implements merge of NodeList and NodeMap."""
    ...


# NodeMap
@overload
def merge_factory(base: NodeMap[TB],
                  other: Node[NO],
                  config: Config,
                  ) -> NodeMap[TR]:
    """Implements merge of NodeMap and NodeMap."""
    ...


@overload
def merge_factory(base: NodeMap[TB],
                  other: NodeList[TO],
                  config: Config,
                  ) -> NodeMap[TR]:
    """Implements merge of NodeMap and NodeMap."""
    ...


@overload
def merge_factory(base: NodeMap[TB],
                  other: NodeMap[TO],
                  config: Config,
                  ) -> NodeMap[TR]:
    """Implements merge of NodeMap and NodeMap."""
    ...


# Realization
def merge_factory(base: TU, other: TU, config: Config) -> AbstractNode:
    if isinstance(base, Node) and isinstance(other, Node):
        return other

    if isinstance(base, Node) and isinstance(other, NodeList):
        return config.merge_different(base, other)

    if isinstance(base, Node) and isinstance(other, NodeMap):
        return config.merge_different(base, other)

    if isinstance(base, NodeList) and isinstance(other, Node):
        return config.merge_different(base, other)

    if isinstance(base, NodeList) and isinstance(other, NodeList):
        return config.merge_list(base, other)

    if isinstance(base, NodeList) and isinstance(other, NodeMap):
        return config.merge_different(base, other)

    if isinstance(base, NodeMap) and isinstance(other, Node):
        return config.merge_different(base, other)

    if isinstance(base, NodeMap) and isinstance(other, NodeList):
        return config.merge_different(base, other)

    if isinstance(base, NodeMap) and isinstance(other, NodeMap):
        for key, value in other.items():
            if key in base:
                base[key] = merge_factory(
                    cast(TU, base[key]),
                    cast(TU, value),
                    config
                )
            else:
                base[key] = value
        return base

    return other
