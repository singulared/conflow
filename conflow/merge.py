"""
Implements merge functionality for every type of Nodes.

base: Layer instance that will be extend or override.
other: Layer instance that will be use for extend or override base.
policy: Enum option that define extend ot override operations.
"""
from conflow.manager import Config
from conflow.node import Node, NodeList, NodeMap, T, TP
from conflow.dispatcher import Dispatch

from typing import Any, Callable

dispatch: Dispatch[type, Callable[..., Any]] = Dispatch()


@dispatch(Node, Node, Config)
def merge_factory(base: Node[T],
                  other: Node[TP],
                  config: Config,
                  ) -> Node[TP]:
    """
    Implements merge of Node with Node.

    Use only Override policy.
    """
    return other


@dispatch(Node, NodeList, Config)  # type: ignore[no-redef]
def merge_factory(base: Node[T],
                  other: Node[TP],
                  config: Config,
                  ) -> Node[TP]:
    """
    Implements merge of Node with Node.

    Use only Override policy.
    """
    return config.merge_list(base, other)


@dispatch(NodeList, NodeList, Config)  # type: ignore[no-redef]
def merge_factory(base: NodeList[T],
                  other: NodeList[TP],
                  config: Config,
                  ) -> NodeList[T]:
    """
    Implements merge of NodeList with NodeList.

    Use both policies.
    """
    return config.merge_list(base, other)


@dispatch(NodeMap, NodeMap, Config)  # type: ignore[no-redef]
def merge_factory(base: NodeMap[T],
                  other: NodeMap[TP],
                  config: Config,
                  ) -> NodeMap[T]:
    """
    Implements merge of NodeMap with NodeMap.

    Use only Extend policy.
    """
    for key, value in other.items():
        if key in base:
            base[key] = merge_factory(base[key], value, config)
        else:
            base[key] = value

    return base
