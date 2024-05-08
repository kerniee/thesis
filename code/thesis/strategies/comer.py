import random

from .ct import CT


class Comer(CT):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __next__(self) -> dict:
        r = random.random()
        if r > self._mr_probability:
            return super().__next__()
        else:
            return super().__next__()
