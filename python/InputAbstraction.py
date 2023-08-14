class abstractedInput:
    def abstractInput():
        # This function should return a list of all the inputs
        # that are currently being pressed.
        return []
class systemTypeInfo:
    def __init__(self, name, version, inputAbstraction):
        self.name = name
        self.version = version
        self.inputAbstraction = inputAbstraction

