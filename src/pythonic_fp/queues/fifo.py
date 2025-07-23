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

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar

from pythonic_fp.circulararray.resizing import CA
from pythonic_fp.fptools.maybe import MayBe

__all__ = ['FIFOQueue', 'fifo_queue']

D = TypeVar('D')


class FIFOQueue[D]:
    """module fifo

    Stateful First In First Out (FIFO) queue data structure.
    Initial data instantiated in natural FIFO order.

    - O(1) length determination
    - in a Boolean context, true if not empty, false if empty
    - will automatically resize itself larger when needed
    - neither indexable nor sliceable by design
    - O(1) pushes and pops

    """
    __slots__ = ('_ca',)

    def __init__(self, *dss: Iterable[D]) -> None:
        """
        :param dss: takes one or no iterables
        :raises ValueError: if more than 1 iterable is given
        """
        if (size := len(dss)) > 1:
            msg = f'FIFOQueue expects at most 1 iterable argument, got {size}'
            raise ValueError(msg)
        self._ca = CA(dss[0]) if size == 1 else CA()

    def __bool__(self) -> bool:
        return len(self._ca) > 0

    def __len__(self) -> int:
        return len(self._ca)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FIFOQueue):
            return False
        return self._ca == other._ca

    def __iter__(self) -> Iterator[D]:
        return iter(list(self._ca))

    def __repr__(self) -> str:
        if len(self) == 0:
            return 'FIFOQueue()'
        return 'FIFOQueue(' + ', '.join(map(repr, self._ca)) + ')'

    def __str__(self) -> str:
        return '<< ' + ' < '.join(map(str, self)) + ' <<'

    def copy(self) -> FIFOQueue[D]:
        """Copy.

        :returns: shallow copy of the FIFOQueue
        """
        return FIFOQueue(self._ca)

    def push(self, *ds: D) -> None:
        """Push an item onto FIFOQueue."""
        self._ca.pushr(*ds)

    def pop(self) -> MayBe[D]:
        """Pop oldest item from FIFOQueue.

        :returns: MayBe of item popped from queue
        """
        if self._ca:
            return MayBe(self._ca.popl())
        return MayBe()

    def peak_last_in(self) -> MayBe[D]:
        """Peak at end. Does not consume data.

        :returns: MayBe of last item in queue
        """
        if self._ca:
            return MayBe(self._ca[-1])
        return MayBe()

    def peak_next_out(self) -> MayBe[D]:
        """Peak at beginning. Does not consume data.

        :returns:  MayBe of next item in queue
        """
        if self._ca:
            return MayBe(self._ca[0])
        return MayBe()

    def fold[T](self, f: Callable[[T, D], T], initial: T | None = None) -> MayBe[T]:
        """Reduces in natural FIFO Order (oldest to newest).

        :param f: reducing function, first argument is for accumulator
        :param initial: optional initial value
        :returns: MayBe of reduced value with f
        """
        if initial is None:
            if not self._ca:
                return MayBe()
        return MayBe(self._ca.foldl(f, initial))

    def map[U](self, f: Callable[[D], U]) -> FIFOQueue[U]:
        """Map f over the FIFOQueue, retain original order.

        :returns: new FIFOQueue
        """
        return FIFOQueue(map(f, self._ca))


def fifo_queue[D](*ds: D) -> FIFOQueue[D]:
    """FIFOQueue factory function."""
    return FIFOQueue(ds)
