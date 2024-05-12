from collections import OrderedDict

from pytest import mark
from testflows.combinatorics import CoveringArray

from thesis.strategies import Comer
from thesis.strategies.mr import MR

params = OrderedDict(
    {
        "highlight": [0, 1],
        "status_bar": [0, 1],
        "bookmarks": [0, 1],
        "smart_tags": [0, 1],
    }
)


def constraint(highlight, status_bar, **kwargs):
    return highlight == status_bar


def mr(bookmarks, smart_tags, **kwargs):
    return OrderedDict({
        "bookmarks": smart_tags,
        "smart_tags": bookmarks,
        **kwargs
    })


@mark.parametrize("testcase", Comer(params, constraint, MR(mr)))
def test_simple(testcase: OrderedDict):
    assert testcase["highlight"] == testcase["status_bar"]


def test_simple_testflow():
    pairs = CoveringArray(params).generate()
    assert len(pairs) == 6
