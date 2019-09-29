from collections import defaultdict, deque
from typing import Optional, TypeVar

from conflow.layer import Layer
from conflow.node import AbstractNode, NodeMap

T = TypeVar('T')


class Config:
    def __init__(self, settings: Optional[dict] = None) -> None:
        self.__map_path_node = defaultdict(deque)
        self.__layers = []
        self.__merged_nodes = {}
        if settings is not None:
            layer = Layer(settings, self.key())
            self.__layers.append(layer)
        self.tree: Optional[AbstractNode[T]] = None

    def key(self):
        return id(self)

    def merge(self, settings: dict) -> 'Config':
        layer = Layer(settings, self.key())
        self.__layers.append(layer)
        return self

    def __merge_layers(self):
        for layer in self.__layers:
            for key, value in layer.flatten():
                self.__map_path_node[key].appendleft(value)

    def __dict_from_merged_layers(self) -> dict:
        for path, node in self.__map_path_node.items():
            current_level = self.__merged_nodes
            for index, key in enumerate(path):
                key_exists = key in current_level
                last_key = index == len(path) - 1
                if not key_exists and last_key:
                    current_level[key] = node[0]
                if not key_exists and not last_key:
                    current_level[key] = {}
                current_level = current_level[key]
        return self.__merged_nodes

    def compile(self) -> None:
        self.__merge_layers()
        merged = self.__dict_from_merged_layers()
        self.tree = NodeMap(self.key(), merged[self.key()])
