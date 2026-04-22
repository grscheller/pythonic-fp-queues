Usage
=====

How to install the package
--------------------------

Install the project into your Python environment:

.. code:: console

   $ pip install pythonic-fp.queues

Importing the package
---------------------

Import the queue classes and "factory functions" into your code.

.. code:: python

    from pythonic_fp.queues.fifo import FIFOQueue, fifo_queue
    from pythonic_fp.queues.lifo import LIFOQueue, lifo_queue
    from pythonic_fp.queues.de import DEQueue, de_queue
