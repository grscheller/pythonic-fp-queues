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

__all__ = ['FIFOQueue', 'fifo_queue']


class FIFOQueue[D]:
    """
    .. admonition:: FIFOQueue

        Stateful First-In-First-Out (FIFO) Queue data structure.

        - O(1) pops
        - O(1) amortized pushes
        - O(1) length determination
        - in a Boolean context, truthy if not empty, falsy if empty
        - will automatically increase storage capacity when needed
        - neither indexable nor sliceable by design

    """

    __slots__ = ('_ca',)

    def __init__(self, *ds: Iterable[D]) -> None:
        """
        .. admonition:: Initializer

            Initialize ``FIFOQueue`` with 0 or 1 iterables to populate
            the queue in natural FIFO order.

        :param ds: Takes 0 or 1 iterable parameters.
        :raises ValueError: When more than one parameter is provided.
        :raises TypeError: When passed a non-iterable parameter.

        """
        if (size := len(ds)) > 1:
            msg = f'FIFOQueue expects at most 1 iterable argument, got {size}'
            raise ValueError(msg)
        self._ca = CA(ds[0]) if size == 1 else CA()

    def __bool__(self) -> bool:
        """
        .. admonition:: Truthiness

            ``FIFOQueue`` truthy when non-empty, falsy when empty.

        """
        return len(self._ca) > 0

    def __len__(self) -> int:
        """
        .. admonition:: Get length

            Return the number of data elements in the ``FIFOQueue``.

        """
        return len(self._ca)

    def __eq__(self, other: object) -> bool:
        """
        .. admonition:: Equality comparison

            If ``other`` is a ``FIFOQueue`` and the corresponding
            elements of ``self`` and ``other`` compare as equal,
            then return ``True``. Otherwise return ``False``.

        :returns: ``self == other``

        """
        if not isinstance(other, FIFOQueue):
            return False
        return self._ca == other._ca

    def __iter__(self) -> Iterator[D]:
        """
        .. admonition:: Iteration

            Iterate over current state in natural FIFO order.

        :returns: An iterator of the data.

        """
        return iter(list(self._ca))

    def __repr__(self) -> str:
        """
        .. admonition:: String representation

            Construct a string to reproduce the ``FIFOQueue``. 

        :returns: The string 'FIFOQueue(repr(a), repr(b), ..., repr(c))'
                  where a, b, ..., c are the queue's contents.

        """
        if len(self) == 0:
           return 'FIFOQueue()'
        return 'FIFOQueue(' + ', '.join(map(repr, self._ca)) + ')'

    def __str__(self) -> str:
        """
        .. admonition:: User string

            Construct a string meaningful to an end user.

        :returns: The string '<< str(a) < str(b) <...< str(c) <<'
                  where a, b, ..., c are the queue's contents.

        """
        return '<< ' + ' < '.join(map(str, self)) + ' <<'

    def copy(self) -> 'FIFOQueue[D]':
        """
        .. admonition:: Copy

            Shallow copy the ``FIFOQueue``.

        :returns: New ``FIFOQueue`` instance containing the same references.

        """
        return FIFOQueue(self._ca)

    def push(self, *ds: D) -> None:
        """
        .. admonition:: Push

            Push data items onto ``FIFOQueue``.

        :param ds: Items to be pushed onto ''FIFOQueue''.

        """
        self._ca.pushr(*ds)

    def pop(self) -> MayBe[D]:
        """
        .. admonition:: Pop

            Pop oldest data item off of ``FIFOQueue``.

        :returns: ``MayBe`` of popped data item if ``FIFOQueue``
                   was not empty, empty ``MayBe`` otherwise.

        """
        if self._ca:
            return MayBe(self._ca.popl())
        return MayBe()

    def peak_last_in(self) -> MayBe[D]:
        """
        .. admonition:: Peak last

            Peak at newest item on ``FIFOQueue``.

        :returns: ``MayBe`` of newest item on ``FIFOQueue``,
                  empty ``MayBe`` if ``FIFOQueue`` empty.

        """
        if self._ca:
            return MayBe(self._ca[-1])
        return MayBe()

    def peak_next_out(self) -> MayBe[D]:
        """
        .. admonition:: Peak next out

            Peak at oldest data item on ``FIFOQueue``.

        :returns: ``MayBe`` of oldest item on ``FIFOQueue``,
                  empty ``MayBe`` if ``FIFOueue`` empty.

        """
        if self._ca:
            return MayBe(self._ca[0])
        return MayBe()

    @overload
    def fold[T](self, f: Callable[[D, D], D]) -> MayBe[D]: ...
    @overload
    def fold[T](self, f: Callable[[T, D], T], start: T) -> MayBe[T]: ...

    def fold[T](self, f: Callable[[T, D], T], start: T | None = None) -> MayBe[T]:
        """
        .. admonition:: Fold

            Reduces ``FIFOQueue`` in natural FIFO Order, oldest to newest.

        :param f: Reducing function, first argument is for accumulator.
        :param start: Optional starting value.
        :returns: ``MayBe`` of reduced value with ``f``, empty ``MayBe``
                  if ``FIFOQueue`` empty and no starting value given.

        """
        if start is None:
            if not self._ca:
                return MayBe()
            return MayBe(cast(T, self._ca.foldl(cast(Callable[[D, D], D], f))))   # T = D
        return MayBe(self._ca.foldl(f, start))

    def map[U](self, f: Callable[[D], U]) -> 'FIFOQueue[U]':
        """
        .. admonition:: Map

            Map ``f`` over the ``FIFOQueue``, retain original order.

        :param f: Function to map over ``FIFOQueue``.
        :returns: New ``FIFOQueue`` instance.

        """
        return FIFOQueue(map(f, self._ca))


def fifo_queue[D](*ds: D) -> FIFOQueue[D]:
    """
    .. admonition:: Create FIFOQueue

        Factory function to create an ``FIFOQueue``
        instance from the function's arguments.

    :param ds: Initial data to be pushed on in FIFO order.
    :returns: New ``FIFOQueue`` instance.

    """
    return FIFOQueue(ds)
