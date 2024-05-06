from collections import OrderedDict

from testflows.combinatorics import CoveringArray

from thesis.comer.comer import Comer

params = OrderedDict(
    {
        "Highlight": [0, 1],
        "StatusBar": [0, 1],
        "Bookmarks": [0, 1],
        "SmartTags": [0, 1],
    }
)


def test_simple():
    pairs = list(Comer(params))
    assert len(pairs) == 6


def test_simple_testflow():
    pairs = CoveringArray(params).generate()
    assert len(pairs) == 6
