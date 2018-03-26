from typing import Dict, Union, Optional, Iterable, List


ConfigKey = Union[str]
ConfigValue = Union[str, int, float, bool, None]


class ConfigNode:
    def __init__(self, key: ConfigKey, value: ConfigValue = None,
                 parent: Optional['ConfigNode'] = None) -> None:
        """
        Create instance of ConfigNode.

        :param name: Config record name
        :param value: Config record value
        :param parent: parent ConfigNode object
        """
        self._key: ConfigKey = key
        self._value: ConfigValue = value
        self._parent: Optional['ConfigNode'] = parent

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


class ConfigList(ConfigNode):
    def __init__(self, key: ConfigKey, value: List[ConfigValue],
                 parent: Optional[ConfigNode] = None) -> None:
        self._key: ConfigKey = key
        self._values: List[ConfigValue] = value
        self._parent: Optional[ConfigNode] = parent
        self.__nodes: List[ConfigNode] = self.__create_nodes(self._values)

    def __repr__(self) -> str:
        """Representation of ConfigList object"""
        return 'ConfigList({key}, {value})'.format(
            key=repr(self._key), value=repr(self._values))

    def __create_nodes(self, values: List[ConfigValue]) -> List[ConfigNode]:
        """
        Create ConfigNodes for all child values

        :param config: part of configuration tree
        """
        return [ConfigNode(self._key, value, self) for value in values]

    def __getitem__(self, key: int) -> 'ConfigNode':
        """
        Implementation of __getitem__ magic method

        :param key: Access key for data
        """
        return self.__nodes[key]

    def __iter__(self) -> Iterable['ConfigNode']:
        """
        Implement iterator interface for child nodes
        """
        return iter(self.__nodes)

    def __contains__(self, item: ConfigValue) -> bool:
        """
        Implementation of __contains__ magic method

        :param item: Value for checking on existing in configuration
        """
        return item in self.__nodes


class ConfigMap(ConfigNode):
    """
    Class implement container for configuration tree node model.

    Provide interface for access configuration record.
    """
    def __init__(self, key: ConfigKey, value: Dict[ConfigKey, ConfigValue],
                 parent: Optional[ConfigNode] = None) -> None:
        """
        Create instance of ConfigNode.

        :param name: Config record name
        :param value: Config record value
        """
        self._key: ConfigKey = key
        self._values: Dict[ConfigKey, ConfigValue] = value
        self._parent: Optional[ConfigNode] = parent
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

    def __getattr__(self, name: ConfigKey) -> 'ConfigNode':
        """
        Implementation of __getattr__ magic method

        :param name: Attribute name (data access key)
        """
        return self.__nodes.get(name, ConfigNode(None))

    def __getitem__(self, key: ConfigKey) -> 'ConfigNode':
        """
        Implementation of __getitem__ magic method

        :param key: Access key for data
        """
        return self.__nodes[key]

    def __contains__(self, item: ConfigValue) -> bool:
        """
        Implementation of __contains__ magic method

        :param item: Value for checking on existing in configuration
        """
        return item in self.__nodes
