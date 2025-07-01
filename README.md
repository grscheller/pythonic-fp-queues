# Pythonic FP - Queues

Three types of classic queue data structures, part of the
PyPI
[pythonic-fp](https://github.com/grscheller/pythonic-fp/blob/main/README.rst)
Namespace Projects.

Detailed API
[documentation](https://grscheller.github.io/pythonic-fp/maintained/fptools)
on *GH-Pages*.

## Features:

These queues allow iterators to leisurely iterate over inaccessible
copies of their current state while the queues themselves are free to
safely mutate. They are designed to be reasonably "atomic" without
introducing inordinate complexity.

All are more restrictive then the underlying circular array data
structure used to implement them. Developers can focus on the queue's
use case instead of all the "bit fiddling" required to implement
behavior, perform memory management, and handle coding edge cases.

Sometimes the real power of a data structure comes not from what it
empowers you to do, but from what it prevents you from doing to
yourself.

| Class     | Queue Type               |
|:---------:|:------------------------ |
| FIFOQueue | First-In-First-Out Queue |
| LIFOQueue | Last-In-First-Out Queue  |
| DEQueue   | Double-Ended Queue       |

This PyPI project is part of of the grscheller
[pythonic-fp namespace projects](https://grscheller.github.io/pythonic-fp/).

## Documentation

Documentation hosted on
[GitHub Pages](https://grscheller.github.io/pythonic-fp-queues/).

## Copyright and License

Copyright (c) 2023-2025 Geoffrey R. Scheller. Licensed under the Apache
License, Version 2.0. See the LICENSE file for details.
