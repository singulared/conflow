from conflow.policy import (
    MergeDifferentTypesPolicy,
    NotifyDifferentTypesPolicy,
    MergeListPolicy
)


class Config:
    def __init__(self,
                 merge_different=MergeDifferentTypesPolicy.not_strict,
                 merge_list=MergeListPolicy.override,
                 notification=NotifyDifferentTypesPolicy.warning,
                 ) -> None:
        self.merge_different = merge_different
        self.merge_list = merge_list
        self.notification = notification
