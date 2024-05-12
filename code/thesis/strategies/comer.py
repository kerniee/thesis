import random
from collections import OrderedDict
from typing import Any

from constraint import Problem

from .ct import CT, FilterType
from .mr import MR


class Comer(CT):
    def __init__(
            self, parameters: OrderedDict[str, list[Any]],
            constraints: FilterType | list[FilterType] = lambda **x: True,
            mrs: None | MR | list[MR] = None, mr_probability=0.5, **kwargs
    ):
        self._mr_probability = mr_probability
        if isinstance(mrs, MR):
            self.mrs = [mrs]
        else:
            self.mrs = mrs if mrs else []
        super().__init__(parameters, constraints, **kwargs)

    def csp_solver(self, case_pre: OrderedDict) -> OrderedDict | None:
        if not self.mrs:
            return

        problem = Problem()
        keys = []

        for key, value in case_pre.items():
            keys.append(key)
            problem.addVariable(key, [value])
        for key, values in self.parameters.items():
            problem.addVariable(key + "'", values)

        keys = tuple(keys)

        for c in self.constraints:
            # def c_before(*args, _c=c, _keys=keys) -> bool:
            #     kwargs = {k: v for k, v in zip(_keys, args[:len(_keys)])}
            #     return _c(**kwargs)

            def c_after(*args, _c=c, _keys=keys) -> bool:
                kwargs = {k: v for k, v in zip(_keys, args[len(_keys):])}
                return _c(**kwargs)

            # problem.addConstraint(c_before)
            problem.addConstraint(c_after)

        for solution in problem.getSolutionIter():

            answer = OrderedDict()
            for key in keys:
                answer[key] = solution[key + "'"]

            if answer not in self.generated_cases:
                return answer
            else:
                1 == 1

    def __next__(self) -> OrderedDict:
        r = random.random()
        if r > self._mr_probability and self.generated_cases:
            case_pre = random.choice(self.generated_cases)
            solution = self.csp_solver(case_pre)
            if solution:
                self.add_testcase_to_tested(solution)
                return solution

        return OrderedDict(super().__next__())
