CrystalMeta
===========

CrystalMeta is a metaclass, and although you will probably not need to use it directly, it is interesting to know what you can do because of it.

.. testsetup:: *

>>> from datacrystals import CrystalMeta

CrystalMeta is a metaclass (that is a class that define classes), and it is built on top of shards.
Therefore all classes defined with it will be shards:

.. doctest::

>>> class MyShard(metaclass=CrystalMeta):
...     answer: int

>>> s1 = MyShard(answer=42)

>>> s1
MyShard(answer=42)


>>> print(s1)
MyShard
-------
answer: 42


But the metaclass also provide extended behavior on the class itself, that is the type of data:



>>> MyShard
<class '__main__.MyShard[answer: <class 'int'>]'>

>>> MyShard == MyShard
True


So we can use it to do some operations at the type level.
