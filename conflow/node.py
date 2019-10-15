from typing import (Any, Collection, Generic, Iterable, Iterator, List,
                    MutableMapping, Optional, TypeVar, Union, cast, overload)

TK = Union[str, int]
VALUE_TYPES = Optional[Union[str, int, float, bool]]

T = TypeVar('T')
TP = TypeVar('TP')
TT = TypeVar('TT')
TU = Union['NodeList[Any]', 'Node[Any]', 'NodeMap[Any]']
TL = TypeVar('TL')


class AbstractNode(Generic[T]):
    def __call__(self) -> Optional[T]: ...


class Node(AbstractNode[Optional[T]]):
    """
    Base class of Node tree.

    Implement some type of container for generic value
    and basic comparison operation.
    """
    def __init__(self, key: TK,
                 value: Optional[T] = None,
                 parent: Optional[AbstractNode[TP]] = None):
        """
        Create instance of Config Node.

        :param key: Config record name
        :param value: Config record value
        :param parent: parent Node object
        """
        self._key: TK = key
        self._value: Optional[T] = value
        self._parent: Optional[AbstractNode[TP]] = parent

    def __call__(self) -> Optional[T]:
        """
        Implementation of __call__ magic method.

        This method return Node value.
        """
        return self._value

    def __repr__(self) -> str:
        """Representation of Node object."""
        return 'Node({key}, {value})'.format(
            key=repr(self._key), value=repr(self()))

    def __eq__(self, other: object) -> bool:
        """Implementation of == operator."""
        return self() == other

    def __ne__(self, other: object) -> bool:
        """Implementation of != operator."""
        return self() != other

    def __getattr__(self, name: TK) -> AbstractNode[None]:
        """
        Implementation of __getattr__ magic method.

        This method return new empty Node for case of chained access.

        :param name: Attribute name (data access key)
        """
        return Node(name, None)


class NodeList(AbstractNode[Collection[Optional[T]]],
               Collection[AbstractNode[T]]):
    """
    Class implement List container for configuration tree node model.

    Provide interface for access configuration records.
    """
    def __init__(self, key: TK, value: Iterable[T],
                 parent: Optional[AbstractNode[TP]] = None) -> None:
        """
        Create instance of Config List.

        :param key: Config record name
        :param value: Config record values (Iterable)
        :param parent: parent Node object
        """
        self._key: TK = key
        self._parent: Optional[AbstractNode[TP]] = parent
        self.__nodes: List[AbstractNode[T]] = self.__create_nodes(value)

    def __call__(self) -> Collection[Optional[T]]:
        """
        Implementation of __call__ magic method.

        This method return NodeList value.
        """
        return [node() for node in self.__nodes]

    def __repr__(self) -> str:
        """Representation of ConfigList object."""
        return 'NodeList({key}, {value})'.format(
            key=repr(self._key), value=repr(self()))

    def __create_nodes(
            self, values: Iterable[T]) -> List[AbstractNode[T]]:
        """
        Create ConfigNodes for all child values.

        :param values: list of configuration tree values
        """
        return [
            cast(AbstractNode[T], node_factory(
                self._key, value, cast(AbstractNode[T], self)
            )) for value in values
        ]

    def __iter__(self) -> Iterator[AbstractNode[T]]:
        """Implement iterator interface for child nodes."""
        return iter(self.__nodes)

    def __eq__(self, other: object) -> bool:
        """Implementation of == operator."""
        return self.__nodes == other

    def __ne__(self, other: object) -> bool:
        """Implementation of != operator."""
        return self.__nodes != other

    def __contains__(self, item: object) -> bool:
        """
        Implementation of __contains__ magic method.

        :param item: Value for checking on existing in configuration
        """
        return item in self.__nodes

    def __len__(self) -> int:
        """Implementation of __len__ magic method."""
        return len(self.__nodes)

    def __getitem__(self, key: int) -> AbstractNode[T]:
        """
        Implementation of __getitem__ magic method.

        :param key: Access key for data
        """
        return self.__nodes[key]


class NodeMap(AbstractNode[MutableMapping[TK, Optional[T]]],
              MutableMapping[TK, AbstractNode[T]]):
    """
    Class implement Map container for configuration tree node model.

    Provide interface for access configuration records.
    """
    def __init__(self, key: TK, value: MutableMapping[TK, T],
                 parent: Optional[AbstractNode[TP]] = None) -> None:
        """
        Create instance of NodeMap.

        :param key: Config record name
        :param value: Config record value
        """
        self._key: TK = key
        self._parent: Optional[AbstractNode[TP]] = parent
        self.__nodes: MutableMapping[
            TK, AbstractNode[T]] = self.__create_nodes(value)

    def __repr__(self) -> str:
        """Representation of NodeMap object."""
        return 'NodeMap({key}, {value})'.format(
            key=repr(self._key), value=repr(self()))

    def __iter__(self) -> Iterator[TK]:
        """Implement iterator interface for child nodes."""
        return iter(self.__nodes)

    def __len__(self) -> int:
        """Implementation of __len__ magic method."""
        return len(self.__nodes)

    def __call__(self) -> MutableMapping[TK, Optional[T]]:
        """
        Implementation of __call__ magic method.

        This method return NodeMap value.
        """
        return {k: v() for k, v in self.__nodes.items()}

    def __create_nodes(self,
                       config: MutableMapping[TK, T]
                       ) -> MutableMapping[TK, AbstractNode[T]]:
        """
        Create ConfigNodes for all child values.

        :param config: part of configuration tree
        """
        return {key: cast(AbstractNode[T], node_factory(
            key, value, self)) for key, value in config.items()}

    def __getattr__(self, name: TK) -> AbstractNode[T]:
        """
        Implementation of __getattr__ magic method.

        :param name: Attribute name (data access key)
        """
        return self.__nodes.get(name, cast(AbstractNode[T], Node(name)))

    def __contains__(self, item: TT) -> bool:
        """
        Implementation of __contains__ magic method.

        :param item: Value for checking on existing in configuration
        """
        return item in self.__nodes.keys()

    def __getitem__(self, key: TK) -> AbstractNode[T]:
        """
        Implementation of __getitem__ magic method.

        :param key: Access key for data
        """
        return self.__nodes[key]

    def __setitem__(self, key: TK, value: AbstractNode[T]) -> None:
        """
        Implementation of __setitem__ magic method.

        :param key: Access key for data
        :param value: Node, NodeList ot NodeMap
        """
        self.__nodes[key] = value

    def __delitem__(self, key: TK) -> None:
        """
        Implementation of __delitem__ magic method.

        :param key: Access key for data
        """
        del(self.__nodes[key])


@overload
def node_factory(key: TK,
                 value: VALUE_TYPES,
                 parent: Optional[AbstractNode[Any]] = None
                 ) -> Node[VALUE_TYPES]: ...


@overload
def node_factory(key: TK,
                 value: List[T],
                 parent: Optional[AbstractNode[Any]] = None
                 ) -> NodeList[T]: ...


@overload
def node_factory(key: TK,
                 value: MutableMapping[TK, T],
                 parent: Optional[AbstractNode[Any]] = None
                 ) -> NodeMap[T]: ...


@overload
def node_factory(key: TK,
                 value: T,
                 parent: Optional[AbstractNode[Any]] = None
                 ) -> TU: ...


def node_factory(key: TK,
                 value: TL,
                 parent: Optional[AbstractNode[TP]] = None,
                 ) -> TU:
    if isinstance(value, List):
        return NodeList(key, value)
    elif isinstance(value, MutableMapping):
        return NodeMap(key, value)
    return Node(key, value)
