import inspect

from ._collection import _collection_from_class as collection
from ._crystals import datacrystal


# This is just a user helper, nothing fancy should happen here,
# just pointing to the appropriate functionality depending on detected usage
def crystalize(_wrpd):

    # TODO : cover all possible cases in a sensible manner (instance method, class method, static method ?)...

    if inspect.isclass(_wrpd):
        return datacrystal(_wrpd)

    else:
        raise NotImplementedError(_wrpd)
