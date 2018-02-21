
class Factory:
    factory = None
    def get():
        if(Factory.factory is None):
            raise RuntimeError("Factory error : factory is not set")
        return Factory.factory
    def set(other):
        if(Factory.factory is None):
            Factory.factory = other


