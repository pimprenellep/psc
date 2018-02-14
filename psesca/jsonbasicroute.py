from .route import Route, Hold

import json

## Route loaded from a json object.
#
# In this class, the shape parameter of the holds is directly a json structure "as is".
class JSONBasicRoute(Route):
    def __init__(self, jtext):
        l = json.loads(jtext)
        self.holds = [Hold(x=h[1], y=h[0], shape=h[2:]) for h in l]
        self.holds.sort(key=lambda h : h.y)


