DataCrystals Tutorial
=====================

DataCrystals provide slightly different data structure implementation than basic Python.
Although they can be a bit more subtle and some details might not be apparent to the untrained eye,
they are more strict, but more understandable, and can be used in many situations.

"Just show me the code !" you say... Well, ok, here we go.

.. testsetup:: *

   import datacrystals

DataCrystals use a similar syntax to dataclasses (and indeed use dataclasses under the hood)
These classes can be instantiated as usual, and are nicely printable on a terminal

Doctest example:

.. doctest::

    >>> @datacrystals.crystalize
    ... class MyDataCrystal:
    ...     field1: int
    ...     field2: str = "field2_default"
    ...
    >>> print(MyDataCrystal)


Test-Output example:

.. testcode::

   print(MyDataCrystal(field1=42))

This would output:

.. testoutput::

   This parrot wouldn't voom if you put 3000 volts through it!
