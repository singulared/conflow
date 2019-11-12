from typing import Callable, NoReturn, TypeVar

from conflow.policy import (
    MergeDifferentTypesPolicy,
    NotifyDifferentTypesPolicy,
    MergeListPolicy
)

T = TypeVar('T')
TP = TypeVar('TP')


class Config:
    def __init__(self,
                 merge_different: Callable[..., NoReturn] =
                 MergeDifferentTypesPolicy.not_strict,
                 merge_list: Callable[[T, TP], TP] =
                 MergeListPolicy.override,
                 notification: Callable[..., None] =
                 NotifyDifferentTypesPolicy.warning,
                 ) -> None:
        self.merge_different = merge_different
        self.merge_list = merge_list
        self.notification = notification
