"""
Implements merge functionality for every type of Nodes.

base: Layer instance that will be extend or override.
other: Layer instance that will be use for extend or override base.
policy: Enum option that define extend ot override operations.
"""
from conflow.manager import Config
from conflow.node import Node, NodeList, NodeMap, T, TP, TU, TT

from typing import overload, cast


# Node
@overload
def merge_factory(base: Node[T],
                  other: Node[TP],
                  config: Config,
                  ) -> Node[TP]:
    """Implements merge of Node and Node."""
    ...


@overload
def merge_factory(base: Node[T],
                  other: NodeList[TP],
                  config: Config,
                  ) -> NodeList[TP]:
    """Implements merge of Node and NodeList."""
    ...


@overload
def merge_factory(base: Node[T],
                  other: NodeMap[TP],
                  config: Config,
                  ) -> NodeMap[TP]:
    """Implements merge of Node and NodeMap."""
    ...


# NodeList
@overload
def merge_factory(base: NodeList[T],
                  other: Node[TP],
                  config: Config,
                  ) -> Node[TP]:
    """Implements merge of NodeList and Node."""
    ...


@overload
def merge_factory(base: NodeList[T],
                  other: NodeList[TP],
                  config: Config,
                  ) -> NodeList[TT]:
    """Implements merge of NodeList and NodeList."""
    ...


@overload
def merge_factory(base: NodeList[T],
                  other: NodeMap[TP],
                  config: Config,
                  ) -> NodeMap[TP]:
    """Implements merge of NodeList and NodeMap."""
    ...


# NodeMap
@overload
def merge_factory(base: NodeMap[T],
                  other: Node[TP],
                  config: Config,
                  ) -> NodeMap[TP]:
    """Implements merge of NodeMap and NodeMap."""
    ...


@overload
def merge_factory(base: NodeMap[T],
                  other: NodeList[TP],
                  config: Config,
                  ) -> NodeMap[TP]:
    """Implements merge of NodeMap and NodeMap."""
    ...


@overload
def merge_factory(base: NodeMap[T],
                  other: NodeMap[TP],
                  config: Config,
                  ) -> NodeMap[TT]:
    """Implements merge of NodeMap and NodeMap."""
    ...


# Realization
def merge_factory(base: TU, other: TU, config: Config) -> TU:
    if isinstance(base, Node) and isinstance(other, Node):
        return other

    if isinstance(base, Node) and isinstance(other, NodeList):
        return config.merge_different(base, other)

    if isinstance(base, Node) and isinstance(other, NodeMap):
        return config.merge_different(base, other)

    if isinstance(base, NodeList) and isinstance(other, Node):
        return config.merge_different(base, other)

    if isinstance(base, NodeList) and isinstance(other, NodeList):
        return config.merge_list(base, other)  # type: ignore

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
