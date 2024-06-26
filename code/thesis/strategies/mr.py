from typing import Callable, OrderedDict


class MR:
    def __init__(
        self,
        in_relation: Callable[..., OrderedDict],
        out_relation: Callable[..., OrderedDict] = lambda t: t,
    ):
        self.in_relation = in_relation
        self.out_relation = out_relation

    def follow_up(self, test_case: OrderedDict) -> OrderedDict:
        return self.in_relation(test_case)

    def apply(self, test_case_output: OrderedDict) -> OrderedDict:
        return self.out_relation(test_case_output)
