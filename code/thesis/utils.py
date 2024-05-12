import inspect
from collections import OrderedDict
from typing import NamedTuple, Callable


def to_ordered_dict(t: NamedTuple) -> OrderedDict:
    fields = t._fields  # noqa
    return OrderedDict({k: v for k, v in zip(fields, list(t))})


def get_number_of_pos_args(f: Callable):
    sig = inspect.signature(f)
    return sum(1 for param in sig.parameters.values() if param.kind == param.POSITIONAL_OR_KEYWORD)
