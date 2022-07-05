from numpy import NaN

class Module ():
    
    def __init__(self, name = 'NAN'):
        self.name = name
        self.params  = []
        self.inputs  = []
        self.outputs = []

class Pin:
    def __init__(self, name = 'NAN', size = 1):
        self.name  = name
        self.size  = size

        if self.size > 1:
            self.type = 'bus'
        else:
            self.type = 'wire'

class Param:
    def __init__(self, name = 'NAN', value = 0):
        self.name  = name
        self.value = value