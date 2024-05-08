from collections import OrderedDict
from typing import NamedTuple


def to_ordered_dict(t: NamedTuple) -> OrderedDict:
    fields = t._fields
    return OrderedDict({k: v for k, v in zip(fields, list(t))})
