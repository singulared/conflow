from typing import MutableMapping


class From(MutableMapping):
    """Implement basic logic for parsing and serving values."""
    def __init__(self, *args, **kwargs):
        self.map = {}
        self.parse()

    def __getitem__(self, key):
        """
        Implementation of __getitem__ magic method.

        :param key: Access key for data
        """
        return self.map[key]

    def __setitem__(self, key, value):
        """
        Implementation of __setitem__ magic method.

        :param key: Access key for data
        :param value: int or str
        """
        self.map.__setitem__(self, key, value)

    def __delitem__(self, *args, **kwargs):
        self.map.__delitem__(*args, **kwargs)

    def __iter__(self):
        """Implement iterator interface for map."""
        return iter(self.map)

    def __len__(self):
        """Implementation of __len__ magic method."""
        return len(self.map)

    def parse(self):
        """Fill `map`."""
        raise NotImplementedError
