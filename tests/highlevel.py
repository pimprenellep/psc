#!/usr/bin/env python3

from context import Application, Factory, DefaultFactory, DummyController

class HLFactory(DefaultFactory):
    def buildController(self, *args):
        return DummyController(*args)

Factory.set(HLFactory())

r = Application().tests(None)
exit(r)
