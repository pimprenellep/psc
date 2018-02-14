from .route import Route, Hold

import json

## Route loaded from a json object.
#
# In this class, the shape parameter of the holds is directly a json structure "as is".
class JSONBasicRoute(Route):
    def __init__(self, jtext):
        l = json.loads(jtext)
        self.holds = map(lambda h : Hold(*h), l)


