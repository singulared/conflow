from typing import MutableMapping, Union, TypeVar, Dict, Iterator

TK = Union[str, int]
T = TypeVar('T')


class From(MutableMapping[TK, T]):
    """
    Various `From*` implementations allow you to load data from different
    sources and convert them into dictionaries, that will be used
    to create layers.

    Basic implementation is required to implement the MutableMapping protocol.
    """
    def __init__(self) -> None:
        self.map: Dict[TK, T] = {}
        self.parse()

    def __getitem__(self, key: TK) -> T:
        """
        Implementation of __getitem__ magic method.

        :param key: Access key for data
        """
        return self.map[key]

    def __setitem__(self, key: TK, value: T) -> None:
        """
        Implementation of __setitem__ magic method.

        :param key: Access key for data
        :param value: int or str
        """
        self.map[key] = value

    def __delitem__(self, key: TK) -> None:
        """
        Implementation of __delitem__ magic method.

        :param key: Access key for data
        """
        del self.map[key]

    def __iter__(self) -> Iterator[TK]:
        """Implement iterator interface for map."""
        return iter(self.map)

    def __len__(self) -> int:
        """Implementation of __len__ magic method."""
        return len(self.map)

    def parse(self) -> None:
        """Fill `map`."""
        raise NotImplementedError
