Beap
====

Beap aka biparental heap (https://en.wikipedia.org/wiki/Beap) is an
[implicit data structure][1] which allows efficient insertion and searching
of elements, while not requiring any more space than the data elements
themselves. Efficient searching and insertion are supported by clever
arrangement of elements in the array which backs the beap structure,
and clever algorithms utilizing this arrangement.

Beap is further elaboration of the ideas of [heap][2] data structure
(which allows for efficient insertion and finding minimum/maximum, but
not efficient searching for an arbitrary element). It was originally
[described][3] by researchers Ian Munro and Hendra Suwanda. Howerver,
it's quite hard to find an implementation of this data structure. Nor
it's easy to implement it based on the original paper, because, following
a good academic tradition, the paper is rather terse, incomplete,
inconsistent and has errata.

This project is an implementation of Beap using Python3, written by
Paul Sokolovsky and distributed under the terms of OpenSource MIT license.
It's intended to be a reference implementation, i.e. written more for
clarity and testability rather than optimized. It's accompanied by
detailed unit tests. The idea is that this implementation can serve
as the basis for more efficient implementation, if such is needed.

For more information on implicit data structures, see
https://github.com/pfalcon/awesome-implicit-data-structures .


[1]: https://en.wikipedia.org/wiki/Implicit_data_structure
[2]: https://en.wikipedia.org/wiki/Heap_(data_structure)
[3]: http://www.sciencedirect.com/science/article/pii/0022000080900379
