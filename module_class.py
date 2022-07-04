from numpy import NaN

class Module ():
    
    param_name  = []
    param_size  = []

    def __init__(self, name = 'NAN'):
        self.name = name
        self.inputs  = []
        self.outputs = []



class Pin:
    def __init__(self, name, size = 1, isBus = False):
        self.name  = name
        self.size  = size
        self.isBus = isBus

class Param:
    def __init__(self, name, value):
        self.name  = name
        self.value = value