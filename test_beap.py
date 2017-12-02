# Run with nosetests3
from beap import Beap


def test_span_indexes():
    assert Beap.span(0) == (0, 0)
    assert Beap.span(1) == (1, 2)
    assert Beap.span(2) == (3, 5)
    assert Beap.span(3) == (6, 9)
    assert Beap.span(4) == (10, 14)
    # Size of span of height i is i + 1
    for i in range(100):
        start, end = Beap.span(i)
        assert end - start + 1 == i + 1
