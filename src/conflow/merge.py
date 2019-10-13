"""
Implements merge functionality for every type of Nodes.

base: Layer instance that will be extend or override.
other: Layer instance that will be use for extend or override base.
policy: Enum option that define extend ot override operations.
"""
from conflow.node import Node, NodeList, NodeMap
from conflow.policy import MergePolicy
from conflow.dispatcher import Dispatch

dispatch = Dispatch()


@dispatch(Node, Node, MergePolicy)
def merge_factory(base: Node,
                  other: Node,
                  policy: MergePolicy
                  ) -> Node:
    """
    Implements merge of Node with Node.

    Use only Override policy.
    """
    return other


@dispatch(NodeList, NodeList, MergePolicy)
def merge_factory(base: NodeList,
                  other: NodeList,
                  policy: MergePolicy
                  ) -> NodeList:
    """
    Implements merge of NodeList with NodeList.

    Use both policies.
    """
    return (
        other if policy == MergePolicy.OVERRIDE
        else NodeList(base._key, [*base, *other])
    )


@dispatch(NodeMap, NodeMap, MergePolicy)
def merge_factory(base: NodeMap,
                  other: NodeMap,
                  policy: MergePolicy
                  ) -> NodeMap:
    """
    Implements merge of NodeMap with NodeMap.

    Use only Extend policy.
    """
    for key, value in other.items():
        if key in base:
            base[key] = merge_factory(base[key], value, policy)
        else:
            base[key] = value

    return base
