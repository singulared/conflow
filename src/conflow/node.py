from typing import Union, Optional, Iterable, TypeVar, Generic, List
from typing import Iterator, Mapping, Collection, cast


TK = Union[str, int]
TV = Optional[Union[str, int, float, bool]]

T = TypeVar('T')
TP = TypeVar('TP')
TT = TypeVar('TT')


class AbstractNode(Generic[T]):
    @property
    def value(self) -> Optional[T]: ...

    def compile(self) -> T: ...


class Node(AbstractNode[Optional[T]]):
    """
    Base class of Node tree

    Implement some type of container for generic value
    and basic comparsion operation.
    """
    def __init__(self, key: TK,
                 value: Optional[T] = None,
                 parent: Optional[AbstractNode[TP]] = None):
        """
        Create instance of Config Node.

        :param name: Config record name
        :param value: Config record value
        :param parent: parent Node object
        """
        self._key: TK = key
        self._value: Optional[T] = value
        self._parent: Optional[AbstractNode[TP]] = parent

    @property
    def value(self) -> Optional[T]:
        """
        Property for accessing configuration node value
        """
        return self._value

    def __repr__(self) -> str:
        """Representation of Node object"""
        return 'Node({key}, {value})'.format(
            key=repr(self._key), value=repr(self.value))

    def compile(self) -> Optional[T]:
        """Method for construction of original python value"""
        return self.value

    def __eq__(self, other: object) -> bool:
        """Implementation of == operator"""
        return self.value == other

    def __ne__(self, other: object) -> bool:
        """Implementation of != operator"""
        return self.value != other


class NodeList(AbstractNode[Collection[T]], Collection[AbstractNode[T]]):
    """
    Class implement List container for configuration tree node model.

    Provide interface for access configuration records.
    """
    def __init__(self, key: TK, value: Iterable[T],
                 parent: Optional[AbstractNode[TP]] = None) -> None:
        """
        Create instance of Config List.

        :param name: Config record name
        :param value: Config record values (Iterable)
        :param parent: parent Node object
        """
        self._key: TK = key
        self._parent: Optional[AbstractNode[TP]] = parent
        self.__nodes: List[AbstractNode[T]] = self.__create_nodes(value)

    def __repr__(self) -> str:
        """Representation of ConfigList object"""
        return 'NodeList({key}, {value})'.format(
            key=repr(self._key), value=repr(self.compile()))

    def compile(self) -> Collection[T]:
        """Method return Node value represented by Python object"""
        return [node.compile() for node in self.__nodes]

    def __create_nodes(
            self, values: Iterable[T]) -> List[AbstractNode[T]]:
        """
        Create ConfigNodes for all child values

        :param value: list of configuration tree values
        """
        return [node_factory(self._key, value, self) for value in values]

    def __iter__(self) -> Iterator[AbstractNode[T]]:
        """
        Implement iterator interface for child nodes
        """
        return iter(self.__nodes)

    def __eq__(self, other: object) -> bool:
        """Implementation of == operator"""
        return self.__nodes == other

    def __ne__(self, other: object) -> bool:
        """Implementation of != operator"""
        return self.__nodes != other

    def __contains__(self, item: object) -> bool:
        """
        Implementation of __contains__ magic method

        :param item: Value for checking on existing in configuration
        """
        return item in self.__nodes

    def __len__(self) -> int:
        """
        Implementation of __len__ magic method
        """
        return len(self.__nodes)

    def __getitem__(self, key: int) -> AbstractNode[T]:
        """
        Implementation of __getitem__ magic method
        :param key: Access key for data
        """
        return self.__nodes[key]


class NodeMap(AbstractNode[Mapping[TK, T]], Mapping[TK, AbstractNode[T]]):
    """
    Class implement Map container for configuration tree node model.

    Provide interface for access configuration records.
    """
    def __init__(self, key: TK, value: Mapping[TK, T],
                 parent: Optional[AbstractNode[TP]] = None) -> None:
        """
        Create instance of ConfigNode.

        :param name: Config record name
        :param value: Config record value
        """
        self._key: TK = key
        self._parent: Optional[AbstractNode[TP]] = parent
        self.__nodes: Mapping[TK, AbstractNode[T]] = self.__create_nodes(value)

    def __repr__(self) -> str:
        """Representation of ConfigMap object"""
        return 'ConfigMap({key}, {value})'.format(
            key=repr(self._key), value=repr(self._values))

    def __iter__(self) -> Iterator[TK]:
        """
        Implement iterator interface for child nodes
        """
        return iter(self.__nodes)

    def __len__(self) -> int:
        """
        Implementation of __len__ magic method
        """
        return len(self.__nodes)

    def __create_nodes(self, config: Mapping[TK, T]
                       ) -> Mapping[TK, AbstractNode[T]]:
        """
        Create ConfigNodes for all child values

        :param config: part of configuration tree
        """
        return {key: node_factory(
            key, value, self) for key, value in config.items()}

    def __getattr__(self, name: TK) -> AbstractNode[T]:
        """
        Implementation of __getattr__ magic method

        :param name: Attribute name (data access key)
        """
        return self.__nodes.get(name, cast(AbstractNode[T], Node(name)))

    def __contains__(self, item: TT) -> bool:
        """
        Implementation of __contains__ magic method

        :param item: Value for checking on existing in configuration
        """
        return item in self.__nodes.keys()

    def __getitem__(self, key: TK) -> AbstractNode[T]:
        """
        Implementation of __getitem__ magic method
        :param key: Access key for data
        """
        return self.__nodes[key]


def node_factory(key: TK,
                 value: TT,
                 parent: Optional[AbstractNode[TP]] = None,
                 ) -> AbstractNode[TT]:
    if isinstance(value, List):
        return cast(AbstractNode[TT], NodeList(key, value))
    elif isinstance(value, Mapping):
        return cast(AbstractNode[TT], NodeMap(key, value))
    return cast(AbstractNode[TT], Node(key, value))


if __name__ == '__main__':
    node = node_factory('test', [1, 2, 3, 4])
    print(node.value)
    len(node)
