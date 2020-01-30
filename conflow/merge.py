"""
Implements merge functionality for every type of Nodes.

base: Layer instance that will be extend or override.
other: Layer instance that will be use for extend or override base.
policy: Enum option that define extend ot override operations.
"""
from typing import overload, cast, TypeVar, Union

from conflow.manager import Config
from conflow.node import Node, NodeList, NodeMap, AbstractNode
from conflow.policy import MergeListPolicy


NB = TypeVar('NB', int, float, str, bool, None)
NO = TypeVar('NO', int, float, str, bool, None)
TB = TypeVar('TB')
TO = TypeVar('TO')
TU = TypeVar('TU')
TY = TypeVar('TY')
TR = Union[
    Node[NO],
    NodeList[TO],
    NodeMap[TO],
    Node[NO],
    NodeList[Union[TB, TO]],
    NodeMap[Union[TB, NO]],
    NodeMap[Union[TB, TO]],
]


# Node
#  @overload
#  def merge_factory(base: Node[NB],
                  #  other: Node[NO],
                  #  config: Config,
                  #  ) -> Node[NO]:
    #  """Implements merge of Node and Node."""
    #  ...


#  @overload
#  def merge_factory(base: Node[NB],
                  #  other: NodeList[TO],
                  #  config: Config,
                  #  ) -> NodeList[TO]:
    #  """Implements merge of Node and NodeList."""
    #  ...


#  @overload
#  def merge_factory(base: Node[NB],
                  #  other: NodeMap[TO],
                  #  config: Config,
                  #  ) -> NodeMap[TO]:
    #  """Implements merge of Node and NodeMap."""
    #  ...


#  # NodeList
#  @overload
#  def merge_factory(base: NodeList[TB],
                  #  other: Node[NO],
                  #  config: Config,
                  #  ) -> Node[NO]:
    #  """Implements merge of NodeList and Node."""
    #  ...


#  @overload
#  def merge_factory(base: NodeList[TB],
                  #  other: NodeList[TO],
                  #  config: Config,
                  #  ) -> NodeList[Union[TB, TO]]:
    #  """Implements merge of NodeList and NodeList."""
    #  ...


#  @overload
#  def merge_factory(base: NodeList[TB],
                  #  other: NodeMap[TO],
                  #  config: Config,
                  #  ) -> NodeMap[TO]:
    #  """Implements merge of NodeList and NodeMap."""
    #  ...


#  # NodeMap
#  @overload
#  def merge_factory(base: NodeMap[TB],
                  #  other: Node[NO],
                  #  config: Config,
                  #  ) -> NodeMap[Union[TB, NO]]:
    #  """Implements merge of NodeMap and NodeMap."""
    #  ...


#  @overload
#  def merge_factory(base: NodeMap[TB],
                  #  other: NodeList[TO],
                  #  config: Config,
                  #  ) -> NodeMap[Union[TB, TO]]:
    #  """Implements merge of NodeMap and NodeList."""
    #  ...


#  @overload
#  def merge_factory(base: NodeMap[TB],
                  #  other: NodeMap[TO],
                  #  config: Config,
                  #  ) -> NodeMap[Union[TB, TO]]:
    #  """Implements merge of NodeMap and NodeMap."""
    #  ...


# Realization
#  def merge_factory(base: Union[Node[NB], NodeList[TB], NodeMap[TB]],
                  #  other: Union[Node[NO], NodeList[TO], NodeMap[TO]],
                  #  config: Config) -> TR[NO, TO, TB]:
def merge_factory(base: AbstractNode[TB],
                  other: AbstractNode[TO],
                  config: Config) -> AbstractNode[TU]:
    if isinstance(base, Node) and isinstance(other, Node):
        return other

    if isinstance(base, Node) and isinstance(other, NodeList):
        #  return config.merge_different(base, other)
        return other

    if isinstance(base, Node) and isinstance(other, NodeMap):
        #  return config.merge_different(base, other)
        return other

    if isinstance(base, NodeList) and isinstance(other, Node):
        #  return config.merge_different(base, other)
        return other

    if isinstance(base, NodeList) and isinstance(other, NodeList):
        #  return config.merge_list(base, other)
        #  return cast(NodeList[Union[TB, TO]],
        #  MergeListPolicy.extend(base, other))
        return other

    if isinstance(base, NodeList) and isinstance(other, NodeMap):
        #  return config.merge_different(base, other)
        return other

    if isinstance(base, NodeMap) and isinstance(other, Node):
        #  return config.merge_different(base, other)
        return other

    if isinstance(base, NodeMap) and isinstance(other, NodeList):
        #  return config.merge_different(base, other)
        return other

    if isinstance(base, NodeMap) and isinstance(other, NodeMap):
        for key, value in other.items():
            if key in base:
                base[key] = merge_factory(base[key], value, config)
            else:
                base[key] = value
        return base
    return other
