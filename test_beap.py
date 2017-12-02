# Run with nosetests3
from beap import Beap, VerifiedBeap


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


def test_invariants():
    # Data from Ian Munro's "ImpSODA06.ppt" presentation, Slide 3,
    # with mistake corrected (21 and 22 not in beap order).
    beap_data = [
    72,
    68, 63,
    44, 62, 55,
    33, 22, 32, 51,
    13, 18, 21, 19, 22,
    11, 12, 14, 17, 9, 13,
     3,  2, 10
    ]
    beap = VerifiedBeap()
    beap.arr = beap_data.copy()
    beap.height = 6
    beap.check_invariants()

    beap.arr[0], beap.arr[1] = beap.arr[1], beap.arr[0]
    try:
        beap.check_invariants()
        failed = True
    except AssertionError:
        failed = False
    assert not failed, "Invariant checks don't work"

    beap.arr = beap_data.copy()
    beap.arr[0], beap.arr[len(beap.arr) - 1] = beap.arr[len(beap.arr) - 1], beap.arr[0]
    try:
        beap.check_invariants()
        failed = True
    except AssertionError:
        failed = False
    assert not failed, "Invariant checks don't work"
