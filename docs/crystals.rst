Crystals
========

A Crystal is a collection of shard.
More precisely a collection of shard that can never lose a shard, but only grow by aggregating more shards.
There are different collections, following Python datastructures

Collection
----------
Similar to a set() of data. Shards are unique here.
Optionally you can count the number of occurrence of each instance here, but this can only grow.

Mapping
-------
Similar to a function, or mapping of data, given an index, so that each one refers to only one shard.


Sequence
--------
Similar to a list, or mapping of data given a totally ordered index.
Note the sequence can oly be done on a continuous index, it would just need to be splitted into intervals.
