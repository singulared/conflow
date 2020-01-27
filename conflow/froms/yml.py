import yaml
from typing import Union, TypeVar, Dict, Optional

TK = Union[str, int]
T = TypeVar('T')


def from_yaml(file_name: str, default: Optional[Dict[TK, T]] = None
              ) -> Dict[TK, T]:
    """Use .yaml file as a source."""
    try:
        with open(file_name, 'r') as file_handler:
            yaml_str  = file_handler.read()
            return yaml.safe_load(yaml_str)
    except FileNotFoundError as error:
        if default is None:
            raise FileNotFoundError(error)
        else:
            return default
