# Run with nosetests3
from beap import Beap, VerifiedBeap


# Data from Ian Munro's "ImpSODA06.ppt" presentation, Slide 3,
# with mistake corrected (21 and 22 not in beap order).
BEAP_DATA = [
    72,
    68, 63,
    44, 62, 55,
    33, 22, 32, 51,
    13, 18, 21, 19, 22,
    11, 12, 14, 17, 9, 13,
     3,  2, 10
]

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
    beap = VerifiedBeap()
    beap.arr = BEAP_DATA.copy()
    beap.height = 6
    beap.check_invariants()

    beap.arr[0], beap.arr[1] = beap.arr[1], beap.arr[0]
    try:
        beap.check_invariants()
        failed = True
    except AssertionError:
        failed = False
    assert not failed, "Invariant checks don't work"

    beap.arr = BEAP_DATA.copy()
    beap.arr[0], beap.arr[len(beap.arr) - 1] = beap.arr[len(beap.arr) - 1], beap.arr[0]
    try:
        beap.check_invariants()
        failed = True
    except AssertionError:
        failed = False
    assert not failed, "Invariant checks don't work"


def test_search_once_off():
    beap = VerifiedBeap()
    beap.arr = BEAP_DATA.copy()
    beap.height = 6

    assert beap.search(51) == (9, 3)
    assert beap.search(53) == None


def test_search():
    beap = VerifiedBeap()
    beap.arr = BEAP_DATA.copy()
    beap.height = 6

    for i in range(101):
        res = beap.search(i)
        if i not in BEAP_DATA:
            assert res is None
        else:
            idx, height = res
            assert beap.arr[idx] == i
            assert height <= beap.height
