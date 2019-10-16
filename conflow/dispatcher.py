from typing import Dict, Tuple, TypeVar, Callable, Generic, Any, cast


T = TypeVar('T', bound=type)
FuncType = Callable[..., Any]
F = TypeVar('F', bound=FuncType)


class Dispatch(Generic[T, F]):
    """
    An implementation of dynamic dispatching for Python.

    Inspired by https://www.artima.com/weblogs/viewpost.jsp?thread=101605
    """
    def __init__(self) -> None:
        self.__types_handlers_map: Dict[Tuple[str, ...], F] = {}

    def __call__(self, *types: T) -> F:
        """Memorize types."""

        def decorator(func: F) -> F:
            """
            Fill the map between arguments types and function that can
            handle them.
            """
            types_ = tuple(
                parameter_type.__name__ for parameter_type in types
            )
            self.__types_handlers_map[types_] = func

            def wrapper(*args: Any) -> Any:
                """Return correct handler from map."""
                arg_types = tuple(type(arg).__name__ for arg in args)
                function = self.__types_handlers_map[arg_types]
                result = function(*args)
                return result
            return cast(F, wrapper)
        return cast(F, decorator)
