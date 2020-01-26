import yaml
from typing import Optional

from conflow.from_implementations.base import From


class FromYaml(From):
    """Use .yaml file as a source."""
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.yaml_str = Optional[str]
        super().__init__()

    def load_file(self):
        """Read file to string."""
        with open(self.file_name, 'r') as file_handler:
            self.yaml_str  = file_handler.read()

    def parse(self) -> None:
        """Fill `map`."""
        self.load_file()
        self.map = yaml.safe_load(self.yaml_str )
