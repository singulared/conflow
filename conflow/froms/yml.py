from typing import TypeVar, Dict, Any

import yaml

T = TypeVar('T')


def from_yaml(file_name: str, required: bool = False) -> Dict[str, Any]:
    """Use .yaml file as a source."""
    try:
        with open(file_name, 'r') as file_handler:
            yaml_str = file_handler.read()
            return yaml.safe_load(yaml_str)
    except FileNotFoundError as error:
        if required:
            raise FileNotFoundError(error)
        else:
            return {}
