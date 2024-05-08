import json
import random
from collections import OrderedDict
from functools import lru_cache
from string import ascii_lowercase, ascii_uppercase, digits, punctuation, whitespace

from mezmorize import Cache

from thesis.strategies import Comer


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
        "len": [0, 1, 10, 50000],
        "has_lower_case": [True, False],
        "has_upper_case": [True, False],
        "has_special_symbols": [True, False],
        "has_digits": [True, False],
        "valid": [True, False],
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
        alphabet += punctuation + get_unicode_alphabet() + whitespace
    if ts["has_digits"]:
        alphabet += digits

    if alphabet == "":
        return ""

    return "".join(random.choice(alphabet) for _ in range(ts["len"]))


def to_function_input(ts: dict, valid_username, valid_password) -> OrderedDict:
    if ts["username_valid"]:
        username = valid_username
    else:
        username = input_field_to_function_input(extract_prefix(ts, "username_"))

    if ts["password_valid"]:
        password = valid_password
    else:
        password = input_field_to_function_input(extract_prefix(ts, "password_"))

    if ts["swapped"]:
        username, password = password, username

    return OrderedDict(
        {
            "username": username,
            "password": password,
        }
    )


def username_len_filter(username_len, username_valid, **kwargs) -> bool:
    if username_len == 0 or username_valid:
        return not (
            kwargs["username_has_lower_case"]
            or kwargs["username_has_upper_case"]
            or kwargs["username_has_special_symbols"]
            or kwargs["username_has_digits"]
        )
    else:
        return (
            kwargs["username_has_lower_case"]
            or kwargs["username_has_upper_case"]
            or kwargs["username_has_special_symbols"]
            or kwargs["username_has_digits"]
        )


def password_len_filter(password_len, password_valid, **kwargs) -> bool:
    if password_len == 0 or password_valid:
        return not (
            kwargs["password_has_lower_case"]
            or kwargs["password_has_upper_case"]
            or kwargs["password_has_special_symbols"]
            or kwargs["password_has_digits"]
        )
    else:
        return (
            kwargs["password_has_lower_case"]
            or kwargs["password_has_upper_case"]
            or kwargs["password_has_special_symbols"]
            or kwargs["password_has_digits"]
        )


cache = Cache(CACHE_TYPE="filesystem", CACHE_DIR=".tmp")


@cache.memoize(9999999)
def get_login_test_cases(valid_username, valid_password) -> list[OrderedDict]:
    abstract = list(
        Comer(params, filter_func=[username_len_filter, password_len_filter])
    )
    return list(
        map(
            lambda testcase: to_function_input(
                testcase, valid_username, valid_password
            ),
            abstract,
        )
    )


def test_quicksort():
    concrete_test_cases = get_login_test_cases("admin", "password")
    assert len(concrete_test_cases) == 26
    with open("login.json", "w+") as f:
        json.dump(concrete_test_cases, f)
