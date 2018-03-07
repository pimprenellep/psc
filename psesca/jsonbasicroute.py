from .native import Route, Hold
from .native import WHAShape

import json

## Route loaded from a json object.
#
# In this class, the shape parameter of the holds is a WHAShape matching the
# first version of image processing
class JSONBasicRoute(Route):
    def __init__(self, jtext):
        l = json.loads(jtext)
        holds = [Hold(x=h[0], y=h[1], shape=WHAShape(*h[2:])) for h in l]
        holds.sort(key=lambda h : h.y)
        super().__init__(holds)
