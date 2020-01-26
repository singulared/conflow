import os
from typing import Union, Optional, TypeVar, MutableMapping, Dict

from conflow.froms.base import From

DELIMITER = '__'

TK = Union[str, int]
T = TypeVar('T')


def try_str_int(value: str) -> Union[str, int]:
    """Try to convert str to int and return int or original str."""
    converted: Optional[int] = None
    try:
        converted = int(value)
    except ValueError:
        pass
    return value if converted is None else converted


class FromEnvironment(From[MutableMapping[TK, T]]):
    """
    Use environment variables as a source.

    Filter all environment variables, leave only those that start with
    the given prefix and build a new layer on them.
    """
    def __init__(self, prefix: str) -> None:
        self.prefix = '{0}_'.format(prefix)
        super().__init__()

    def load_by_prefix(self) -> Dict[str, str]:
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
        joined_path = env_var_name[len(self.prefix):]
        keys = joined_path.split(DELIMITER)
        lower_keys = list(map(
            lambda item: item.lower(), keys
        ))
        reversed_keys = list(reversed(lower_keys))
        current_dict: Dict[TK, T] = self.map
        while len(reversed_keys) > 1:
            key = reversed_keys.pop()
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]
        current_dict[reversed_keys.pop()] = try_str_int(env_var_value)

    def parse(self) -> None:
        """Parse all envs and fill `map`."""
        envs_pairs = self.load_by_prefix()
        for env_var_name, env_var_value in envs_pairs.items():
            self.add_pair(env_var_name, env_var_value)
