from typing import Tuple, Generator, List, overload, TypeVar, Union, Optional

from conflow.node import Node, NodeList, NodeMap, AbstractNode

T = TypeVar('T')
P = TypeVar('P')

TK = Union[str, int]
Path = Tuple[TK, ...]


def path_from(path: Optional[Path], key: TK) -> Path:
    if path is None:
        return key,
    return (*path, key)


@overload
def flatten_tree(path: Optional[Path], node: Node[T]
                 ) -> Generator[Tuple[Path, Node[T]], None, None]: ...


@overload
def flatten_tree(path: Optional[Path], node: NodeList[T]
                 ) -> Generator[Tuple[Path, NodeList[T]], None, None]: ...


@overload
def flatten_tree(path: Optional[Path], node: NodeMap[T]
                 ) -> Generator[Tuple[Path, AbstractNode[P]], None, None]: ...


def flatten_tree(path: Optional[Path], node: AbstractNode[T]
                 ) -> Generator[Tuple[Path, AbstractNode[T]], None, None]:
    if isinstance(node, Node):
        yield path_from(path, node._key), node

    if isinstance(node, NodeList):
        yield path_from(path, node._key), node

    if isinstance(node, NodeMap):
        for child_node in node.values():
            yield from flatten_tree(path_from(path, node._key), child_node)


class Layer:
    def __init__(self, settings: dict, name: TK) -> None:
        self.__tree = NodeMap(name, settings)

    def flatten(self) -> List[Tuple[AbstractNode[T], Path]]:
        return list(flatten_tree(None, self.__tree))
