import os
from typing import Union
from conflow.from_implementations.base_implementation import From

DELIMITER = '__'


def try_str_int(value: str) -> Union[str, int]:
    """Try to convert str to int and return int or original str."""
    try:
        value = int(value)
    except ValueError:
        pass
    return value


class FromEnvironment(From):
    def __init__(self, prefix: str) -> None:
        self.prefix = '{0}_'.format(prefix)
        super().__init__()

    def load_by_prefix(self) -> dict:
        """Load env variables and filter by prefix."""
        envs_pairs = filter(
            lambda item: item[0].startswith(self.prefix),
            os.environ.items()
        )
        return dict(envs_pairs)

    def add_pair(self, env_var_name: str, env_var_value: str) -> None:
        """
        Add to `map` pair keys: value.

        :param env_var_name: delimited keys.
        :param env_var_value: result value.
        """
        path = env_var_name[len(self.prefix):]
        path = path.split(DELIMITER)
        path = list(map(lambda item: item.lower(), path))
        path = list(reversed(path))
        current_dict = self.map
        while len(path) > 1:
            key = path.pop()
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]
        current_dict[path.pop()] = try_str_int(env_var_value)

    def parse(self) -> dict:
        """Parse all envs and fill `map`."""
        envs_pairs = self.load_by_prefix()
        for env_var_name, env_var_value in envs_pairs.items():
            self.add_pair(env_var_name, env_var_value)
        return self.map
