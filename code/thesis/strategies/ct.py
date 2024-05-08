from typing import Any, Callable, OrderedDict

from thesis.allpairs import AllPairs
from thesis.utils import to_ordered_dict

FilterType = Callable[..., bool | None]


class CT(AllPairs):
    def __init__(
        self,
        parameters: OrderedDict[str, list[Any]],
        constraints: FilterType | list[FilterType] = lambda **x: True,
        **kwargs,
    ) -> None:
        self.constraints = (
            constraints if isinstance(constraints, list) else [constraints]
        )

        if not isinstance(constraints, list):
            constraints = [constraints]

        new_constraints = []

        for f in constraints:

            def __filter_func(x: list, _f=f) -> bool:
                if len(parameters) != len(x):
                    return True
                else:
                    filter_input = {k: v for k, v in zip(parameters.keys(), x)}
                    res = _f(**filter_input)
                    return True if res is None else res

            new_constraints.append(__filter_func)

        def new_filter_func(args: list) -> bool:
            return all(new_f(args) for new_f in new_constraints)

        self.generated_cases: list[OrderedDict] = []
        self.parameters = parameters
        super().__init__(parameters=parameters, filter_func=new_filter_func, **kwargs)

    def __next__(self) -> dict:
        case = to_ordered_dict(super().__next__())
        self.generated_cases.append(case)
        return case
