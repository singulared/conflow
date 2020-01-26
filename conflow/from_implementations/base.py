from typing import MutableMapping, Any


class From(MutableMapping):
    """
    Various `From*` implementations allow you to load data from different
    sources and convert them into dictionaries, that will be used
    to create layers.

    Basic implementation is required to implement the MutableMapping protocol.
    """
    def __init__(self, *args, **kwargs) -> None:
        self.map = {}
        self.parse()

    def __getitem__(self, key) -> Any:
        """
        Implementation of __getitem__ magic method.

        :param key: Access key for data
        """
        return self.map[key]

    def __setitem__(self, key, value) -> None:
        """
        Implementation of __setitem__ magic method.

        :param key: Access key for data
        :param value: int or str
        """
        self.map[key] = value

    def __delitem__(self, key) -> None:
        """
        Implementation of __delitem__ magic method.

        :param key: Access key for data
        """
        del self.map[key]

    def __iter__(self) -> None:
        """Implement iterator interface for map."""
        return iter(self.map)

    def __len__(self) -> None:
        """Implementation of __len__ magic method."""
        return len(self.map)

    def parse(self) -> None:
        """Fill `map`."""
        raise NotImplementedError
