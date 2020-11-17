datacrystals
============

Crystallizing Data

Design main points
------------------

* wrap dataclasses to provide typecheck (pydantic) and consistent str/repr interface for human/machine
* provide data structures (bunch of dataclasses instances) that are representable in DataFrame, with a consistent str/repr interface for human/machine
* MAYBE LATER : refine python Type as a "proper type" ( mathematical sense ) and store its witness in a dataframe...
* MAYBE LATER : wrap python functions into a datastructure, to represent its calls / its memoization(cache) as a dataframe...

These data structures come in various forms that are still being defined. Some axes of reflexion:

* Ordering seems prerequisite here
  otherwise it is a set, a type, etc., an abstract thing that doesnt really fit into python mindset
* with unicity enforced (Set), but two unique time measurement cannot be made (in the same location)...
* with repetition recorded (Bag), but time cannot repeat itself...
* Indexed on a specific discrete type (like int)
* Indexed on a continuous type (like time)
* updateable via call() only (one mutation point allows tight control of data)
* async __aiter__() follows the flow of time, whereas __iter__ doesnt (backwards ?)
* more TODO...


We want the mutability of these potentially huge data structures to be tightly controlled,
typed and functional, but without rewriting Python...

We try to follow a "Categorical Spirit" and make it easy for the user to implement containers (cf. Danel Ahman paper),
to help him cleanly interface his python code with anything else (Julia being the first target).

Roadmap
-------

* v0.1 : dataclass wrapping + instances list represented in a dataframe with python's collection interface
* v0.2 : ??
