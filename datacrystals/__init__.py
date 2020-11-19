import inspect

from ._collection import Collection
from ._collection import _collection_from_class as collection
from .shards import shard


# This is just a user helper, nothing fancy should happen here,
# just pointing to the appropriate functionality depending on detected usage
def crystalize(_wrpd):

    # TODO : cover all possible cases in a sensible manner (instance method, class method, static method ?)...

    if inspect.isclass(_wrpd):
        return shard(_wrpd)

    else:
        raise NotImplementedError(_wrpd)


# TODO:
# crystalize/datacrystal -> shard ("makes a class into a shard". shard = elementary/atomic datacrystal)
# collection -> collection (set interface)
# mapping -> mapping (dict interface - require unique index)
# sequence -> sequence (list interface - require ordered index)
# crystalize:
#    - makes a collection/mapping/sequence into a shard, ie. some kind of type casting... (uses shard() or not ??)
#    - makes a (typed) set into a collection
#    - makes a (typed) dict into a mapping
#    - makes a (typed) list into a sequence
#    - makes a normal class into a shard, simply using shard()
#
