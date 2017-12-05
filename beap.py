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

import logging

log = logging.getLogger(__name__)


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

    def search(self, x):
        """Search for element x in beap. If not found, return None.
        Otherwise, return tuple of (idx, height) with array index
        and span height at which the element was found. (Span height
        is returned because it may be needed for some further
        operations, to avoid square root operation which is otherwise
        needed to convert array index to it.)
        """
        h = self.height
        start, end = self.span(h)
        idx = start

        while 1:
            log.debug("search: idx: %d", idx)
            log.debug("search: idx: %d arr[idx]: %s", idx, self.arr[idx])
            if x > self.arr[idx]:
                # "If x is less than the element under consideration, move left
                # one position along the row."
                # These rules are given for weirdly mirrored matrix. They're also
                # for min beap, we so far implement max beap.
                # So: if x is greater than, and move up along the column.
                log.debug("Moving up ^")
                if idx == end:
                    log.debug("Can't move up")
                    return None
                diff = idx - start
                h -= 1
                start, end = self.span(h)
                idx = start + diff
                continue
            elif x < self.arr[idx]:
                # If x exceeds the element, either move down one position along the column or if
                # this is not possible (because we are on the diagonal) then move left and down one position
                # each.
                # => less, move right along the row, or up and right
                log.debug("Moving right ->")

                if idx == len(self.arr) - 1:
                    log.debug("Last el reached, can't move right, moving up instead")
                    diff = idx - start
                    h -= 1
                    start, end = self.span(h)
                    idx = start + diff
                    continue


                diff = idx - start
                new_start, new_end = self.span(h + 1)
                new_idx = new_start + diff + 1
                if new_idx < len(self.arr):
                    h += 1
                    start = new_start
                    end = new_end
                    idx = new_idx
                    continue

                log.debug("Can't move right, moving right-up /")

                if idx == end:
                    log.debug("Can't move right-up")
                    return None

                idx += 1
                continue

            else:
                return (idx, h)


    def filter_up(self, idx, h):
        "Percolate an element up the beap."
        v = self.arr[idx]
        while h:
            start, end = self.span(h)
            left_p = right_p = None
            val_l = val_r = None

            diff = idx - start
            st_p, end_p = self.span(h - 1)

            if idx != start:
                left_p = st_p + diff - 1
                val_l = self.arr[left_p]
            if idx != end:
                right_p = st_p + diff
                val_r = self.arr[right_p]

            log.debug("filter_up: left_p: %s (val: %s) right_p: %s (val: %s)", left_p, val_l, right_p, val_r)

            if val_l is not None and v > val_l and (val_r is None or val_l < val_r):
                self.arr[left_p], self.arr[idx] = self.arr[idx], self.arr[left_p]
                idx = left_p
                h -= 1
            elif val_r is not None and v > val_r:
                self.arr[right_p], self.arr[idx] = self.arr[idx], self.arr[right_p]
                idx = right_p
                h -= 1
            else:
                return

        assert idx == 0


    def insert(self, v):
        "Insert element v into beap."
        start, end = self.span(self.height)
        # If last array element as at the span end, then adding
        # new element grows beap height.
        if len(self.arr) - 1 == end:
            self.height += 1
        self.arr.append(v)

        h = self.height
        idx = len(self.arr) - 1
        return self.filter_up(idx, h)


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
        for i in range(self.height + 1):
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
