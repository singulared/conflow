from typing import Dict, Union, List, Optional, Iterable


ConfigKey = Union[str]
ConfigValue = Union[str, int, float, List, Dict, bool, None]


class ConfigNode:
    """
    Class implement container for configuration tree node model.

    Provide interface for access configuration record.
    """
    def __init__(self, key: ConfigKey, value: ConfigValue = None,
                 parent: Optional['ConfigNode'] = None) -> None:
        """
        Create instance of ConfigNode.

        :param name: Config record name
        :param value: Config record value
        """
        self.__key: ConfigKey = key
        self.__value: ConfigValue = value
        self.__parent: Optional['ConfigNode'] = parent
        self.__nodes: Dict[ConfigKey, 'ConfigNode'] = {}
        if isinstance(value, (dict,)):
            self.__create_nodes(value)

    def __repr__(self) -> str:
        return 'ConfigNode({key}, {value})'.format(
            key=repr(self.__key), value=repr(self.value))

    def __iter__(self) -> Iterable['ConfigNode']:
        """
        Implement iterator interface for child nodes
        """
        return iter(self.__nodes.values())

    def __create_nodes(self, config: Dict[ConfigKey, ConfigValue]) -> None:
        """
        Create ConfigNodes for all child values

        :param config: part of configuration tree
        """
        for key, value in config.items():
            self.__nodes[key] = ConfigNode(key, value, self)

    @property
    def value(self) -> ConfigValue:
        """
        Property for accessing configuration node value
        """
        return self.__value

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
