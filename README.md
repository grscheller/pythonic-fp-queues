# Pythonic FP - Queues

Python package implementing 3 types of queue data structures. This
project is part of the [Developer Tools for Python][1] **pythonic-fp**
namespace projects.

- **Repositories**
  - [dtools.queues][2] project on *PyPI*
  - [Source code][3] on *GitHub*
- **Detailed documentation**
  - [Detailed API documentation][4] on *GH-Pages*

## Overview

Classic queue data structures:

- *module* dtools.queues
  - *module* fifo: First-In-First-Out Queue - FIFOQueue
  - *module* lifo: Last-In-First-Out Queue - LIFOQueue
  - *module* de: Double-Ended Queue - DEQueue

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

[1]: https://github.com/grscheller/pythonic-fp/blob/main/README.md
[2]: https://pypi.org/project/pythonic-fp.queues/
[3]: https://github.com/grscheller/pythonic-fp-queues/
[4]: https://grscheller.github.io/pythonic-fp/maintained/queues/
