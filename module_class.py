from numpy import NaN

class Module ():
    
    param_name  = []
    param_value = []

    def __init__(self, name = 'NAN'):
        self.name = name
        self.input_name  = []
        self.output_name = []
        
        self.input_size  = []
        self.output_size = []

class Pin:
    def __init__(self, name, size = 1):
        self.name  = name
        self.size  = size

        if self.size > 1:
            self.isBus = True
        else:
            self.isBus = False

class Param:
    def __init__(self, name, value):
        self.name  = name
        self.value = value