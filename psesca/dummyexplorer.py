from .explorer import Explorer

# Does nothing but instantiating a controller
class DummyExplorer(Explorer) :
    def __init__(self):
        self.controller = DummyController()
    
