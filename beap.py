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
