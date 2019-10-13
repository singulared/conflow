from collections import Callable

from typing import Dict, Tuple


class Dispatch:
    """
    An implementation of dynamic dispatching for Python.

    Inspired by https://www.artima.com/weblogs/viewpost.jsp?thread=101605
    """
    def __init__(self):
        self.__types_handlers_map: Dict[Tuple[str, ...], Callable] = {}

    def __call__(self, *types):
        """Memorize types."""

        def decorator(func: Callable) -> Callable:
            """
            Fill the map between arguments types and function that can
            handle them.
            """
            types_ = tuple(
                parameter_type.__name__ for parameter_type in types
            )
            self.__types_handlers_map[types_] = func

            def wrapper(*args):
                """Return correct handler from map."""
                arg_types = tuple(type(arg).__name__ for arg in args)
                function = self.__types_handlers_map[arg_types]
                result = function(*args)
                return result
            return wrapper
        return decorator
