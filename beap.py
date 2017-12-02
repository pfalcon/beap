#
# Bi-parental heap (beap) implementation.
# https://en.wikipedia.org/wiki/Beap
#
# The implementation is based on paper "Implicit Data Structures for
# Fast Search and Update" by Ian Munro and Hendra Suwanda.
#

class Beap:

    def __init__(self):
        # Backing array for beap storage
        self.arr = []
        # Current height of beap. Note that height is defined as
        # distance between consecutive layers, so for single-element
        # beap height is 0, and for empty, we initialize it to -1.
        self.height = -1

    # "The i'th block consists of the i elements stored from position
    # (i(i - 1)/2 + 1) through position i(i + 1)/2."
    # These formulas use 1-based i, and return 1-based array index.
    @staticmethod
    def span_1_based(i):
        start = i * (i - 1) // 2 + 1
        end = i * (i + 1) // 2
        return (start, end)

    @staticmethod
    # Convert to use sane zero-based indexes both for "block" (span)
    # and array.
    def span(i):
        """Return start and end (inclusive) of beap span of height i
        (zero-based)."""
        start, end = Beap.span_1_based(i + 1)
        return (start - 1, end - 1)
