#
# Bi-parental heap (beap) implementation.
# https://en.wikipedia.org/wiki/Beap
#
# The implementation is based on paper "Implicit Data Structures for
# Fast Search and Update" by Ian Munro and Hendra Suwanda.
#
# The MIT License (MIT)
#
# Copyright (c) 2017 Paul Sokolovsky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
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


class BeapInvariantsMixIn:

    # "Taking a slightly different point of view, one can interpret
    # this structure as an upper triangular of a matrix (or grid) in
    # which locations 1, 2, 4, 7 ... form the first column and
    # 1, 3, 6, 10 ... the first row. Furthermore, each row and each
    # column are maintained in sorted order."

    def check_row_invar(self):
        total = 0
        for i in range(self.height + 1):
            idx, end = self.span(i)
            row = []
            for j in range(self.height + 1):
                try:
                    row.append(self.arr[idx])
                except IndexError:
                    break
                idx += i + j + 2
            # Max beap
            assert row == sorted(row, reverse=True), "%r vs expected %r" % (row, sorted(row, reverse=True))
            total += len(row)

        assert total == len(self.arr)


    def check_col_invar(self):
        total = 0
        for i in range(self.height + 0):
            start, idx = self.span(i)
            diff = idx - start
            col = []
            for j in range(self.height + 1):
                try:
                    col.append(self.arr[idx])
                except IndexError:
                    break
                idx, e = self.span(i + j + 1)
                idx += diff
            # Max beap
            assert col == sorted(col, reverse=True), "%r vs expected %r" % (col, sorted(col, reverse=True))
            total += len(col)

        assert total == len(self.arr), "%d vs %d" % (total, len(self.arr))


    def check_invariants(self):
        self.check_row_invar()
        self.check_col_invar()


class VerifiedBeap(Beap, BeapInvariantsMixIn):
    pass
