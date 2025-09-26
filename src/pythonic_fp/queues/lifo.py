# Copyright 2023-2024 Geoffrey R. Scheller
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
from pythonic_fp.fptools.function import swap
from pythonic_fp.fptools.maybe import MayBe

__all__ = ['LIFOQueue', 'lifo_queue']


class LIFOQueue[D]:
    """Stateful Last-In-First-Out (LIFO) Queue data structure.

    - O(1) pops
    - O(1) amortized pushes
    - O(1) length determination
    - in a Boolean context, true if not empty, false if empty
    - will automatically increase storage capacity when needed
    - neither indexable nor sliceable by design

    """
    __slots__ = ('_ca',)

    def __init__(self, *dss: Iterable[D]) -> None:
        """
        :param dss: Takes 1 or 0 iterables, initializes data in natural LIFO order.
        :raises ValueError: If more than 1 iterable is given.
        """
        if (size := len(dss)) > 1:
            msg = f'LIFOQueue expects at most 1 iterable argument, got {size}'
            raise ValueError(msg)
        self._ca = CA(dss[0]) if size == 1 else CA()

    def __bool__(self) -> bool:
        return len(self._ca) > 0

    def __len__(self) -> int:
        return len(self._ca)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LIFOQueue):
            return False
        return self._ca == other._ca

    def __iter__(self) -> Iterator[D]:
        return reversed(list(self._ca))

    def __repr__(self) -> str:
        if len(self) == 0:
            return 'LIFOQueue()'
        return 'LIFOQueue(' + ', '.join(map(repr, self._ca)) + ')'

    def __str__(self) -> str:
        return '|| ' + ' > '.join(map(str, self)) + ' ><'

    def copy(self) -> 'LIFOQueue[D]':
        """Shallow copy.

        :returns: Shallow copy of the LIFOQueue.
        """
        return LIFOQueue(reversed(self._ca))

    def push(self, *ds: D) -> None:
        """Push items onto LIFOQueue.

        :param ds: Items to be pushed onto LIFOQueue.
        """
        self._ca.pushr(*ds)

    def pop(self) -> MayBe[D]:
        """Pop newest data item off of LIFOQueue.

        :returns: MayBe of popped item if queue was not empty, empty MayBe otherwise.
        """
        if self._ca:
            return MayBe(self._ca.popr())
        return MayBe()

    def peak(self) -> MayBe[D]:
        """Peak at newest item on queue.

        :returns: MayBe of newest item on queue, empty MayBe if queue empty.
        """
        if self._ca:
            return MayBe(self._ca[-1])
        return MayBe()

    @overload
    def fold[T](self, f: Callable[[D, D], D]) -> MayBe[D]: ...
    @overload
    def fold[T](self, f: Callable[[T, D], T], start: T) -> MayBe[T]: ...

    def fold[T](self, f: Callable[[T, D], T], start: T | None = None) -> MayBe[T]:
        """Reduces LIFOQUEUE in natural LIFO Order, newest to oldest.

        :param f: Reducing function, first argument is for accumulator.
        :param start: Optional starting value.
        :returns: MayBe of reduced value, empty MayBe if queue empty and no starting value given.
        """
        if start is None:
            if not self._ca:
                return MayBe()
            return MayBe(cast(T, self._ca.foldl(cast(Callable[[D, D], D], f))))   # T = D
        return MayBe(self._ca.foldr(swap(f), start))

    def map[U](self, f: Callable[[D], U]) -> 'LIFOQueue[U]':
        """Map f over the LIFOQueue, retain original order.

        :param f: Function to map over queue.
        :returns: New LIFOQueue instance.
        """
        return LIFOQueue(reversed(CA(map(f, reversed(self._ca)))))


def lifo_queue[D](*ds: D) -> LIFOQueue[D]:
    """LIFOQueue factory function.

    :param ds: Initial items pushed on in LIFO order.
    :returns: LIFOQueue with initialized items from ``ds``.
    """
    return LIFOQueue(ds)
