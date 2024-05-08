import random
from collections import OrderedDict

from constraint import Problem

from .ct import CT
from .mr import MR


class Comer(CT):
    def __init__(
        self, *args, mrs: None | MR | list[MR] = None, mr_probability=0.5, **kwargs
    ):
        self._mr_probability = mr_probability
        if isinstance(mrs, MR):
            self.mrs = [mrs]
        else:
            self.mrs = mrs if mrs else []
        super().__init__(*args, **kwargs)

    def csp_solver(self, case_pre: OrderedDict) -> OrderedDict:
        problem = Problem()
        for key, values in self.parameters.items():
            problem.addVariable(key, values)
            problem.addVariable(f"{key}'", values)
        for c in self.constraints:
            problem.addConstraint(c)
        return problem.getSolution()

    def __next__(self) -> OrderedDict:
        r = random.random()
        if r > self._mr_probability and self.generated_cases:
            case_pre = random.choice(self.generated_cases)
            solution = self.csp_solver(case_pre)
            return solution

        return OrderedDict(super().__next__())
