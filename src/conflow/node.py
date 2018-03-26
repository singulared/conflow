from typing import Dict, Union, Optional, Iterable, List


ConfigKey = Union[str]
ConfigValue = Union[str, int, float, bool, None]


class AbstractNode:
    """Pure abstract class needed only for right class hierarchy"""
    pass


class ConfigNode(AbstractNode):
    """
    Class implement Map container for configuration tree node model.

    Provide interface for access configuration record.
    """
    def __init__(self, key: Optional[ConfigKey] = None,
                 value: Optional[ConfigValue] = None,
                 parent: Optional[AbstractNode] = None) -> None:
        """
        Create instance of ConfigNode.

        :param name: Config record name
        :param value: Config record value
        :param parent: parent AbstractNode object
        """
        self._key: Optional[ConfigKey] = key
        self._value: Optional[ConfigValue] = value
        self._parent: Optional[AbstractNode] = parent

    def __repr__(self) -> str:
        """Representation of ConfigNode object"""
        return 'ConfigNode({key}, {value})'.format(
            key=repr(self._key), value=repr(self.value))

    @property
    def value(self) -> ConfigValue:
        """
        Property for accessing configuration node value
        """
        return self._value

    def __eq__(self, other: object) -> bool:
        """Implementation of == operator"""
        return self.value == other

    def __ne__(self, other: object) -> bool:
        """Implementation of != operator"""
        return self.value != other

    def compile(self) -> ConfigValue:
        """Method return Node value represented by Python object"""
        return self.value


class ConfigList(AbstractNode):
    """
    Class implement Map container for configuration tree node model.

    Provide interface for access configuration records.
    """
    def __init__(self, key: ConfigKey, value: List[ConfigValue],
                 parent: Optional[AbstractNode] = None) -> None:
        """
        Create instance of ConfigList.

        :param name: Config record name
        :param value: Config record values (list)
        :param parent: parent AbstractNode object
        """
        self._key: ConfigKey = key
        self._parent: Optional[AbstractNode] = parent
        self.__nodes: List[ConfigNode] = self.__create_nodes(value)

    def __repr__(self) -> str:
        """Representation of ConfigList object"""
        return 'ConfigList({key}, {value})'.format(
            key=repr(self._key), value=repr(self.compile()))

    def compile(self) -> List[ConfigValue]:
        """Method return Node value represented by Python object"""
        return [node.compile() for node in self.__nodes]

    def __create_nodes(self, values: List[ConfigValue]) -> List[ConfigNode]:
        """
        Create ConfigNodes for all child values

        :param value: list of configuration tree values
        """
        return [ConfigNode(self._key, value, self) for value in values]

    def __iter__(self) -> Iterable[ConfigNode]:
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

    def __contains__(self, item: ConfigValue) -> bool:
        """
        Implementation of __contains__ magic method

        :param item: Value for checking on existing in configuration
        """
        return item in self.__nodes

    def __getitem__(self, key: int) -> AbstractNode:
        """
        Implementation of __getitem__ magic method
        :param key: Access key for data
        """
        return self.__nodes[key]


class ConfigMap(AbstractNode):
    """
    Class implement Map container for configuration tree node model.

    Provide interface for access configuration records.
    """
    def __init__(self, key: ConfigKey, value: Dict[ConfigKey, ConfigValue],
                 parent: Optional[AbstractNode] = None) -> None:
        """
        Create instance of ConfigNode.

        :param name: Config record name
        :param value: Config record value
        """
        self._key: ConfigKey = key
        self._values: Dict[ConfigKey, ConfigValue] = value
        self._parent: Optional[AbstractNode] = parent
        self.__nodes: Dict[ConfigKey, ConfigNode] = self.__create_nodes(
            self._values)

    def __repr__(self) -> str:
        """Representation of ConfigMap object"""
        return 'ConfigMap({key}, {value})'.format(
            key=repr(self._key), value=repr(self._values))

    def __iter__(self) -> Iterable['ConfigNode']:
        """
        Implement iterator interface for child nodes
        """
        return iter(self.__nodes.values())

    def __create_nodes(self, config: Dict[ConfigKey, ConfigValue]) -> Dict[
            ConfigKey, ConfigNode]:
        """
        Create ConfigNodes for all child values

        :param config: part of configuration tree
        """
        return {key: ConfigNode(
            key, value, self) for key, value in config.items()}

    def __getattr__(self, name: ConfigKey) -> AbstractNode:
        """
        Implementation of __getattr__ magic method

        :param name: Attribute name (data access key)
        """
        return self.__nodes.get(name, ConfigNode(None))

    def __eq__(self, other: object) -> bool:
        """Implementation of == operator"""
        return self.__nodes == other

    def __ne__(self, other: object) -> bool:
        """Implementation of != operator"""
        return self.__nodes != other

    def __contains__(self, item: ConfigValue) -> bool:
        """
        Implementation of __contains__ magic method

        :param item: Value for checking on existing in configuration
        """
        return item in self.__nodes.values()

    def __getitem__(self, key: ConfigKey) -> 'ConfigNode':
        """
        Implementation of __getitem__ magic method
        :param key: Access key for data
        """
        return self.__nodes[key]
