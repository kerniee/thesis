import random
from typing import Callable, OrderedDict

from thesis.allpairs import AllPairs


class Comer(AllPairs):
    def __init__(self, parameters: list | OrderedDict, *args, mr_probability=1,
                 filter_func: Callable[..., bool | None] = lambda *x: True, **kwargs):
        def __filter_func(x: list) -> bool:
            if len(parameters) != len(x):
                return True
            else:
                return filter_func(*x) is None or filter_func(*x)

        self.__mr_probability = mr_probability
        super().__init__(parameters, *args, filter_func=__filter_func, **kwargs)

    def __next__(self) -> dict:
        r = random.random()
        if r > self.__mr_probability:
            pass
        else:
            return super().__next__()._asdict()
