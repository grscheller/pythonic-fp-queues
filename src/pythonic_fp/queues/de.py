# Copyright 2023-2026 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Callable, Iterable, Iterator
from typing import cast, overload
from pythonic_fp.circulararray.auto import CA
from pythonic_fp.fptools.maybe import MayBe

__all__ = ['DEQueue', 'de_queue']


class DEQueue[D]:
    """
    .. admonition:: DEQueue

        Stateful Double-Ended (DE) Queue data structure.

        - has a left and a right side
        - O(1) pops each end
        - O(1) amortized pushes each end
        - O(1) length determination
        - in a Boolean context, truthy if not empty, falsy if empty
        - will automatically increase storage capacity when needed
        - neither indexable nor sliceable by design

    """

    __slots__ = ('_ca',)

    def __init__(self, *ds: Iterable[D]) -> None:
        """
        .. admonition:: Initializer

            Initialize ``DEQueue`` with 0 or 1 iterables to populate
            the queue left (front) to right (rear).

        :param ds: Takes 0 or 1 iterable parameters.
        :raises ValueError: When more than one parameter is provided.
        :raises TypeError: When passed a non-iterable parameter.

        """
        if (size := len(ds)) > 1:
            msg = f'DEQueue expects at most 1 argument, got {size}'
            raise ValueError(msg)
        self._ca = CA(ds[0]) if size == 1 else CA()

    def __bool__(self) -> bool:
        """
        .. admonition:: Truthiness

            Queue truthy when non-empty, falsy when empty.

        """
        return len(self._ca) > 0

    def __len__(self) -> int:
        """
        .. admonition:: Get length

            Return the number of data elements in the ``DEQueue``.

        """
        return len(self._ca)

    def __eq__(self, other: object) -> bool:
        """
        .. admonition:: Equality comparison

            If ``other`` is a ``DEQueue`` and the corresponding
            elements of ``self`` and ``other`` compare as equal,
            then return ``True``. Otherwise return ``False``.

        :returns: ``self == other``

        """
        if not isinstance(other, DEQueue):
            return False
        return self._ca == other._ca

    def __iter__(self) -> Iterator[D]:
        """
        .. admonition:: Iteration

            Iterate over current state left to right.

        :returns: An iterator of the data.

        """
        return iter(list(self._ca))

    def __reversed__(self) -> Iterator[D]:
        """
        .. admonition:: Iteration

            Iterate over current state right to left.

        :returns: An iterator of the data.

        """
        return reversed(list(self._ca))

    def __repr__(self) -> str:
        """
        .. admonition:: String representation

            Construct a string to reproduce the ``DEQueue``. 

        :returns: The string 'DEQueue(repr(a), repr(b), ..., repr(c))'
                  where a, b, ..., c are the queue's contents.

        """
        if len(self) == 0:
            return 'DEQueue()'
        return 'DEQueue(' + ', '.join(map(repr, self._ca)) + ')'

    def __str__(self) -> str:
        """
        .. admonition:: User string

            Construct a string meaningful to an end user.

        :returns: The string '>< str(a) | str(b) |...| str(c) ><'
                  where a, b, ..., c are the queue's contents.

        """
        return '>< ' + ' | '.join(map(str, self)) + ' ><'

    def copy(self) -> 'DEQueue[D]':
        """
        .. admonition:: Copy

            Shallow copy the ``DEQueue``.

        :returns: New ``DEQueue`` instance containing the same references.

        """
        return DEQueue(self._ca)

    def pushl(self, *ds: D) -> None:
        """
        .. admonition:: Push left

            Push data onto left side of ``DEQueue``.

        :param ds: Data to be pushed onto ``DEQueue`` from the left.

        """
        self._ca.pushl(*ds)

    def pushr(self, *ds: D) -> None:
        """
        .. admonition:: Push right

            Push data onto right side of ``DEQueue``.

        :param ds: Data to be pushed onto ``DEQueue`` from the right.

        """
        self._ca.pushr(*ds)

    def popl(self) -> MayBe[D]:
        """
        .. admonition:: Pop left

            Pop next item from left side ``DEQueue``, if it exists.

        :returns: ``MayBe`` of popped item if queue was not empty,
                  empty ``MayBe`` otherwise.

        """
        if self._ca:
            return MayBe(self._ca.popl())
        return MayBe()

    def popr(self) -> MayBe[D]:
        """
        .. admonition:: Pop right

            Pop next item off right side ''DEQueue``, if it exists.

        :returns: ``MayBe`` of popped item if queue was not empty,
                  empty ``MayBe`` otherwise.

        """
        if self._ca:
            return MayBe(self._ca.popr())
        return MayBe()

    def peakl(self) -> MayBe[D]:
        """
        .. admonition:: Peak left

            Peak left side of ``DEQueue``. Does not consume item.

        :returns: ``MayBe`` of leftmost item if queue not empty,
                  empty ``MayBe`` otherwise.

        """
        if self._ca:
            return MayBe(self._ca[0])
        return MayBe()

    def peakr(self) -> MayBe[D]:
        """
        .. admonition:: Peak right

            Peak right side of ``DEQueue``. Does not consume item.

        :returns: ``MayBe`` of rightmost item if queue not empty,
                  empty ``MayBe`` otherwise.

        """
        if self._ca:
            return MayBe(self._ca[-1])
        return MayBe()

    @overload
    def foldl[L](self, f: Callable[[D, D], D]) -> MayBe[D]: ...
    @overload
    def foldl[L](self, f: Callable[[L, D], L], start: L) -> MayBe[L]: ...

    def foldl[L](self, f: Callable[[L, D], L], start: L | None = None) -> MayBe[L]:
        """
        .. admonition:: Fold left

            Reduce ``DEQueue`` left to right.

        :param f: Reducing function, first argument is for accumulator.
        :param start: Optional starting value.
        :returns: ``MayBe`` of reduced value with ``f``, empty ``MayBe`` if
                  queue empty and no starting value given.

        """
        if start is None:
            if not self._ca:
                return MayBe()
            return MayBe(cast(L, self._ca.foldl(cast(Callable[[D, D], D], f))))   # L = D
        return MayBe(self._ca.foldl(f, start))

    @overload
    def foldr[R](self, f: Callable[[D, D], D]) -> MayBe[D]: ...
    @overload
    def foldr[R](self, f: Callable[[D, R], R], start: R) -> MayBe[R]: ...

    def foldr[R](self, f: Callable[[D, R], R], start: R | None = None) -> MayBe[R]:
        """
        .. admonition:: Fold right

            Reduce ``DEQueue`` right to left.

        :param f: Reducing function, second argument is for accumulator.
        :param start: Optional starting value.
        :returns: ``MayBe`` of reduced value with ``f``, empty ``MayBe``
                  if queue empty and no starting value given.

        """
        if start is None:
            if not self._ca:
                return MayBe()
            return MayBe(cast(R, self._ca.foldr(cast(Callable[[D, D], D], f))))  # R = D
        return MayBe(self._ca.foldr(f, start))

    def map[U](self, f: Callable[[D], U]) -> 'DEQueue[U]':
        """
        .. admonition:: Map

            Map left to right.

            .. tip::

                Order map done does not matter if ``f`` is pure.

        :param f: Function to map over queue.
        :returns: New ``DEQueue`` instance, retain original order.

        """
        return DEQueue(map(f, self._ca))


def de_queue[D](*ds: D) -> DEQueue[D]:
    """
    .. admonition:: Create DEQueue

        Factory function to create a ``DEQueue``
        instance from the function's arguments.

    :param ds: Initial data to be pushed on right to left.
    :returns: A new ``DEQueue`` instance.

    """
    return DEQueue(ds)
