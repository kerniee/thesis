from collections import OrderedDict

from thesis.strategies import Comer

params = OrderedDict(
    {
        "st": [";", ""],
        "q": ['"', "'", "%22", "%27", ";", ""],
        "whsp": [" ", "/**/", "%20", "%09", "%A0", "%0A", "%0B", "%0C", "%0D", ""],
    }
)


def to_function_input(ts: dict) -> OrderedDict:
    return OrderedDict({"query": ts["st"] + ts["q"] + ts["whsp"]})


def get_sql_test_cases() -> list[OrderedDict]:
    abstract = list(Comer(params))
    return list(
        map(
            lambda testcase: to_function_input(testcase),
            abstract,
        )
    )


def test_sql():
    print(*get_sql_test_cases(), sep="\n")
    assert len(get_sql_test_cases()) == 60
