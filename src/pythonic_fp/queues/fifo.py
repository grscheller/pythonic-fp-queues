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
from pythonic_fp.fptools.maybe import MayBe

__all__ = ['FIFOQueue', 'fifo_queue']


class FIFOQueue[D]:
    """Stateful First-In-First-Out (FIFO) Queue data structure.

    - O(1) pops
    - O(1) amortized pushes
    - O(1) length determination
    - in a Boolean context, truthy if not empty, falsy if empty
    - will automatically increase storage capacity when needed
    - neither indexable nor sliceable by design

    """

    __slots__ = ('_ca',)

    def __init__(self, *dss: Iterable[D]) -> None:
        """
        :param dss: Takes 1 or 0 iterables, initializes items in natural FIFO order.
        :raises ValueError: If more than 1 iterable is given.
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

    def copy(self) -> 'FIFOQueue[D]':
        """Shallow copy.

        :returns: Shallow copy of the FIFOQueue.
        """
        return FIFOQueue(self._ca)

    def push(self, *ds: D) -> None:
        """Push items onto FIFOQueue.

        :param ds: Items to be pushed onto FIFOQueue.
        """
        self._ca.pushr(*ds)

    def pop(self) -> MayBe[D]:
        """Pop oldest data item off of FIFOQueue.

        :returns: MayBe of popped data item if queue was not empty, empty MayBe otherwise.
        """
        if self._ca:
            return MayBe(self._ca.popl())
        return MayBe()

    def peak_last_in(self) -> MayBe[D]:
        """Peak at newest item on queue.

        :returns: MayBe of newest item on queue, empty MayBe if queue empty.
        """
        if self._ca:
            return MayBe(self._ca[-1])
        return MayBe()

    def peak_next_out(self) -> MayBe[D]:
        """Peak at oldest data item on queue.

        :returns: MayBe of oldest item on queue, empty MayBe if queue empty.
        """
        if self._ca:
            return MayBe(self._ca[0])
        return MayBe()

    @overload
    def fold[T](self, f: Callable[[D, D], D]) -> MayBe[D]: ...
    @overload
    def fold[T](self, f: Callable[[T, D], T], start: T) -> MayBe[T]: ...

    def fold[T](self, f: Callable[[T, D], T], start: T | None = None) -> MayBe[T]:
        """Reduces FIFOQueue in natural FIFO Order, oldest to newest.

        :param f: Reducing function, first argument is for accumulator.
        :param start: Optional starting value.
        :returns: MayBe of reduced value, empty MayBe if queue empty and no starting value given.
        """
        if start is None:
            if not self._ca:
                return MayBe()
            return MayBe(cast(T, self._ca.foldl(cast(Callable[[D, D], D], f))))   # T = D
        return MayBe(self._ca.foldl(f, start))

    def map[U](self, f: Callable[[D], U]) -> 'FIFOQueue[U]':
        """Map f over the FIFOQueue, retain original order.

        :param f: Function to map over queue.
        :returns: New FIFOQueue instance.
        """
        return FIFOQueue(map(f, self._ca))


def fifo_queue[D](*ds: D) -> FIFOQueue[D]:
    """FIFOQueue factory function.

    :param ds: Initial items pushed on in FIFO order.
    :returns: FIFOQueue with initialized items from ``ds``.
    """
    return FIFOQueue(ds)
