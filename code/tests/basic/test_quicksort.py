import random
from collections import OrderedDict

from thesis.strategies import Comer

params = OrderedDict(
    {
        "same_number": [0, range(1, 20), range(20, 40)],
        "negative": [0, range(1, 20), range(20, 40)],
        "positive": [0, range(1, 20), range(20, 40)],
        "zero": [0, range(1, 5), range(5, 10)],
        "extreme_values": [0, range(1, 5)],
        "order": ["positive", "negative", "out of order"],
    }
)


def to_concrete_values(ts: dict) -> dict:
    new_ts = dict()
    for key, value in ts.items():
        concrete_value = value
        if isinstance(value, range):
            concrete_value = random.choice(value)
        new_ts[key] = concrete_value
    return new_ts


def to_function_input(ts: dict) -> list:
    func_input = []
    func_input.extend([random.randint(-1000, 1000)] * ts["same_number"])
    func_input.extend(random.randint(-1000, -1) for _ in range(ts["negative"]))
    func_input.extend(random.randint(1, 1000) for _ in range(ts["positive"]))
    func_input.extend(0 for _ in range(ts["zero"]))
    func_input.extend(
        random.randint(-(10**100), 10**100) for _ in range(ts["extreme_values"])
    )
    if ts["order"] == "out of order":
        func_input.sort(key=lambda x: random.randint(0, 1) == 0)
    if ts["order"] == "positive":
        func_input.sort()
    if ts["order"] == "negative":
        func_input.sort(reverse=True)
    return func_input


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        left = [x for x in arr[1:] if x < pivot]
        right = [x for x in arr[1:] if x >= pivot]
        return quicksort(left) + [pivot] + quicksort(right)


def test_quicksort():
    def f(same_number, zero, **_):
        if same_number == 0:
            return zero == 0

    abstract_test_cases = list(Comer(params, filter_func=f))
    concrete_test_cases = list(map(to_concrete_values, abstract_test_cases))
    assert len(concrete_test_cases) == 15
    for testcase in concrete_test_cases:
        func_input = to_function_input(testcase)
        assert sorted(func_input) == quicksort(func_input)
