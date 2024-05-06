import random
from collections import OrderedDict
from functools import lru_cache
from string import ascii_lowercase, ascii_uppercase, digits, punctuation, whitespace

from thesis.comer.comer import Comer


def add_prefix(ts: dict, prefix: str) -> dict:
    return {prefix + key: value for key, value in ts.items()}


def extract_prefix(ts: dict, prefix: str) -> dict:
    return {
        key.replace(prefix, "", 1): value
        for key, value in ts.items()
        if key.startswith(prefix)
    }


input_field_params = OrderedDict(
    {
        "len": [0, 1, 5, 10, 50, 500, 50000],
        "has_lower_case": [True, False],
        "has_upper_case": [True, False],
        "has_special_symbols": [True, False],
        "has_digits": [True, False],
        "has_unicode": [True, False],
        "has_whitespace": [True, False],
    }
)

params = OrderedDict(
    {
        **add_prefix(input_field_params, "username_"),
        **add_prefix(input_field_params, "password_"),
        "swapped": [True, False],
    }
)


@lru_cache
def get_unicode_alphabet():
    include_ranges = [
        (0x0021, 0x0021),
        (0x0023, 0x0026),
        (0x0028, 0x007E),
        (0x00A1, 0x00AC),
        (0x00AE, 0x00FF),
        (0x0100, 0x017F),
        (0x0180, 0x024F),
        (0x2C60, 0x2C7F),
        (0x16A0, 0x16F0),
        (0x0370, 0x0377),
        (0x037A, 0x037E),
        (0x0384, 0x038A),
        (0x038C, 0x038C),
    ]

    alphabet = [
        chr(code_point)
        for current_range in include_ranges
        for code_point in range(current_range[0], current_range[1] + 1)
    ]
    return "".join(alphabet)


def input_field_to_function_input(ts: dict) -> str:
    alphabet = ""
    if ts["has_lower_case"]:
        alphabet += ascii_lowercase
    if ts["has_upper_case"]:
        alphabet += ascii_uppercase
    if ts["has_special_symbols"]:
        alphabet += punctuation
    if ts["has_digits"]:
        alphabet += digits
    if ts["has_unicode"]:
        alphabet += get_unicode_alphabet()
    if ts["has_whitespace"]:
        alphabet += whitespace

    if alphabet == "":
        return ""

    return "".join(random.choice(alphabet) for _ in range(ts["len"]))


def to_function_input(ts: dict) -> list:
    username = input_field_to_function_input(extract_prefix(ts, "username_"))
    password = input_field_to_function_input(extract_prefix(ts, "password_"))
    if ts["swapped"]:
        username, password = password, username
    return [username, password]


def test_quicksort():
    def username_len_filter(username_len, **kwargs):
        if username_len == 0:
            return not (
                kwargs["username_has_lower_case"]
                and kwargs["username_has_upper_case"]
                and kwargs["username_has_special_symbols"]
                and kwargs["username_has_digits"]
                and kwargs["username_has_unicode"]
                and kwargs["username_has_whitespace"]
            )

    concrete_test_cases = list(Comer(params, filter_func=username_len_filter))
    print(len(concrete_test_cases))
    # for testcase in concrete_test_cases:
    #     func_input = to_function_input(testcase)
    # func_output = sorted(func_input)
    # print(testcase, func_input)
