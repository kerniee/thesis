from typing import Callable, OrderedDict

from thesis.allpairs import AllPairs

FilterType = Callable[..., bool | None]


class CT(AllPairs):
    def __init__(
        self,
        parameters: OrderedDict,
        mr_probability: int = 1,
        filter_func: FilterType | list[FilterType] = lambda **x: True,
        **kwargs,
    ) -> None:
        if not isinstance(filter_func, list):
            filter_func = [filter_func]

        new_filter_func_list = []

        for f in filter_func:

            def __filter_func(x: list, _f=f) -> bool:
                if len(parameters) != len(x):
                    return True
                else:
                    filter_input = {k: v for k, v in zip(parameters.keys(), x)}
                    res = _f(**filter_input)
                    return True if res is None else res

            new_filter_func_list.append(__filter_func)

        def new_filter_func(args: list) -> bool:
            return all(new_f(args) for new_f in new_filter_func_list)

        self._mr_probability = mr_probability
        self.generated_cases: list[dict] = []
        super().__init__(parameters=parameters, filter_func=new_filter_func, **kwargs)

    def __next__(self) -> dict:
        case = super().__next__()._asdict()
        self.generated_cases.append(case)
        return case
