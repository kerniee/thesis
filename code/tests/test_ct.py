from collections import OrderedDict

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
