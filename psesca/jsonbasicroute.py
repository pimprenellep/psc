from .route import Route, Hold
from .wha_shape import WHAShape

import json

## Route loaded from a json object.
#
# In this class, the shape parameter of the holds is a WHAShape matching the
# first version of image processing
class JSONBasicRoute(Route):
    def __init__(self, jtext):
        l = json.loads(jtext)
        self.holds = [Hold(x=h[0], y=h[1], shape=WHAShape(*h[2:])) for h in l]
        self.holds.sort(key=lambda h : h.y)


