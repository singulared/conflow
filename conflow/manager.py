from conflow.policy import (
    MergeDifferentTypesPolicy,
    NotifyDifferentTypesPolicy,
    MergeListPolicy
)


class Config:
    def __init__(self,
                 merge_different: MergeDifferentTypesPolicy =
                 MergeDifferentTypesPolicy.NOT_STRICT,

                 merge_list: MergeListPolicy =
                 MergeListPolicy.OVERRIDE,

                 notification: NotifyDifferentTypesPolicy =
                 NotifyDifferentTypesPolicy.WARNING,
                 ) -> None:
        self.merge_different = merge_different
        self.merge_list = merge_list
        self.notification = notification
