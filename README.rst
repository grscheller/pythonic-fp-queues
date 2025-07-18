Pythonic FP - Queues
====================

PyPI project
`pythonic-fp.queues
<https://pypi.org/project/pythonic-fp.queues>`_.

Three data structures with queue-like behaviors.

+-----------+--------------------------+
|   Class   |      Type of Queue       |
+===========+==========================+
| FIFOQueue | First-In-First-Out Queue |
+-----------+--------------------------+
| LIFOQueue | Last-In-First-Out Queue  |
+-----------+--------------------------+
| DEQueue   |    Double-Ended Queue    |
+-----------+--------------------------+

Each with capabilities:

- O(1) pushes and pops
- O(1) length determination
- in a Boolean context

  - true if not empty
  - false if empty

- will resize themselves larger when needed
- not indexable or sliceable by design

This PyPI project is part of of the grscheller
`pythonic-fp namespace projects
<https://github.com/grscheller/pythonic-fp/blob/main/README.md>`_

Documentation
-------------

Documentation for package
`GitHub Pages
<https://grscheller.github.io/pythonic-fp/queues/API/development/build/html/releases.html>`_
hosted on GitHub pages.

Copyright and License
---------------------

Copyright (c) 2023-2025 Geoffrey R. Scheller. Licensed under the Apache
License, Version 2.0. See the LICENSE file for details.
