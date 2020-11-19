Shards
======

A shard is a simple dataclass, with few extra methods.

.. testsetup:: *

>>> from datacrystals import shard

You can define it as you would a normal dataclass, except that it has to be frozen,
and various methods are already defined for simple REPL interactive usage:

.. doctest::

>>> @shard
... class MyShard:
...     answer: int

>>> s1 = MyShard(answer=42)

>>> s2 = MyShard(answer=51)

>>> s1
MyShard(answer=42)


>>> s2
MyShard(answer=51)


>>> print(s1)
MyShard
-------
answer: 42

>>> print(s2)
MyShard
-------
answer: 51





There is nothing really fancy about it just yet, and you can use it as a dataclass.
