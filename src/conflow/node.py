from typing import Sequence, Union, Optional, Iterable, TypeVar, Generic
from typing import Iterator, Mapping


ConfigKey = Union[str, int]
ConfigValue = Optional[Union[str, int, float, bool]]

T = TypeVar('T')
TP = TypeVar('TP')


class Node(Generic[T]):
    """Base class needed only for right class hierarchy"""
    def __init__(self, key: ConfigKey,
                 value: Optional[T] = None,
                 parent: Optional['Node[TP]'] = None) -> None:
        """
        Create instance of ConfigNode.

        :param name: Config record name
        :param value: Config record value
        :param parent: parent Node object
        """
        self._key: ConfigKey = key
        self._value: Optional[T] = value
        self._parent: Optional[Node[TP]] = parent

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


class NodeList(Node[Sequence]):
    """
    Class implement Map container for configuration tree node model.

    Provide interface for access configuration records.
    """
    def __init__(self, key: ConfigKey, value: Sequence[T],
                 parent: Optional[Node[TP]] = None) -> None:
        """
        Create instance of ConfigList.

        :param name: Config record name
        :param value: Config record values (list)
        :param parent: parent Node object
        """
        super().__init__(key, value, parent)
        self.__nodes: Sequence[Node[T]] = self.__create_nodes(value)

    def __repr__(self) -> str:
        """Representation of ConfigList object"""
        return 'ConfigList({key}, {value})'.format(
            key=repr(self._key), value=repr(self.compile()))

    def compile(self) -> Sequence[Optional[T]]:
        """Method return Node value represented by Python object"""
        return [node.compile() for node in self.__nodes]

    def __create_nodes(
            self, values: Sequence[T]) -> Sequence[Node[T]]:
        """
        Create ConfigNodes for all child values

        :param value: list of configuration tree values
        """
        return [Node(self._key, value, self) for value in values]

    def __iter__(self) -> Iterator[Node[T]]:
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

    def __contains__(self, item: T) -> bool:
        """
        Implementation of __contains__ magic method

        :param item: Value for checking on existing in configuration
        """
        return item in self.__nodes

    def __getitem__(self, key: int) -> Node[T]:
        """
        Implementation of __getitem__ magic method
        :param key: Access key for data
        """
        return self.__nodes[key]


class NodeMap(Node[Mapping]):
    """
    Class implement Map container for configuration tree node model.

    Provide interface for access configuration records.
    """
    def __init__(self, key: ConfigKey, value: Mapping[ConfigKey, T],
                 parent: Optional[Node[TP]] = None) -> None:
        """
        Create instance of ConfigNode.

        :param name: Config record name
        :param value: Config record value
        """
        super().__init__(key, value, parent)
        self.__nodes: Mapping[ConfigKey, Node[T]] = self.__create_nodes(value)

    def __repr__(self) -> str:
        """Representation of ConfigMap object"""
        return 'ConfigMap({key}, {value})'.format(
            key=repr(self._key), value=repr(self._values))

    def __iter__(self) -> Iterable[Node[T]]:
        """
        Implement iterator interface for child nodes
        """
        return iter(self.__nodes.values())

    def __create_nodes(self, config: Mapping[ConfigKey, T]) -> Mapping[
            ConfigKey, Node[T]]:
        """
        Create ConfigNodes for all child values

        :param config: part of configuration tree
        """
        return {key: Node(
            key, value, self) for key, value in config.items()}

    def __getattr__(self, name: ConfigKey) -> Node[T]:
        """
        Implementation of __getattr__ magic method

        :param name: Attribute name (data access key)
        """
        return self.__nodes.get(name, Node(name))

    def __contains__(self, item: ConfigValue) -> bool:
        """
        Implementation of __contains__ magic method

        :param item: Value for checking on existing in configuration
        """
        return item in self.__nodes.values()

    def __getitem__(self, key: ConfigKey) -> Node[T]:
        """
        Implementation of __getitem__ magic method
        :param key: Access key for data
        """
        return self.__nodes[key]
