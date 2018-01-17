from typing import Dict, Union, List, Optional


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
        self.__nodes: Dict[ConfigKey, 'ConfigNode'] = {}
        self.__parent: Optional[ConfigNode] = parent
        if isinstance(value, (dict,)):
            self.__create_nodes(value)

    def __repr__(self) -> str:
        return 'ConfigNode(\'{name}\', {value})'.format(
            name=self.__name, value=self.__value)

    def __create_nodes(self, config: Dict) -> None:
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
