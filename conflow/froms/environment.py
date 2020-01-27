import os
from typing import Union, Optional, TypeVar, Dict

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


def load_by_prefix(prefix: str) -> Dict[str, str]:
    """Load env variables and filter by prefix."""
    envs_pairs = filter(
        lambda item: item[0].startswith(prefix),
        os.environ.items()
    )
    start_index = len(prefix) + 1
    prepared_envs_pairs = map(
        lambda item: (item[0][start_index:], item[1]),
        envs_pairs
    )
    return dict(prepared_envs_pairs)


def add_pair(env_map: Dict[TK, T], env_var_name: str, env_var_value: str
             ) -> Dict[TK, T]:
    """
    Add to `map` pair keys: value.

    :param env_map: updated dictionary.
    :param env_var_name: delimited keys.
    :param env_var_value: result value.
    """
    keys = env_var_name.split(DELIMITER)
    lower_keys = list(map(
        lambda item : item.lower(), keys
    ))
    reversed_keys = list(reversed(lower_keys))
    current_dict: Dict[TK, T] = env_map
    while len(reversed_keys) > 1 :
        key = reversed_keys.pop()
        if key not in current_dict :
            current_dict[key] = {}
        current_dict = current_dict[key]
    current_dict[reversed_keys.pop()] = try_str_int(env_var_value)
    return env_map


def from_env(prefix: str) -> Dict[TK, T]:
    envs_pairs = load_by_prefix(prefix)
    env_map = {}
    for env_var_name, env_var_value in envs_pairs.items():
        add_pair(env_map, env_var_name, env_var_value)
    return env_map
