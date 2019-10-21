from collections import Callable

from conflow.node import TU
from conflow.policy import (
    MergeDifferentTypesPolicy,
    NotifyDifferentTypesPolicy,
    MergeListPolicy
)


class Config:
    def __init__(self,
                 merge_different: Callable[[TU, TU], TU] =
                 MergeDifferentTypesPolicy.NOT_STRICT.value,

                 merge_list: Callable[[TU, TU], TU] =
                 MergeListPolicy.OVERRIDE.value,

                 notification: Callable[[TU, TU], None] =
                 NotifyDifferentTypesPolicy.WARNING.value,
                 ) -> None:
        self.merge_different = merge_different
        self.merge_list = merge_list
        self.notification = notification
