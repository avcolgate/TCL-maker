class Module:
    def __init__(self, name = ''):
        self.name = name
        self.params  = []
        self.inputs  = []
        self.outputs = []

    def print(self):
        print(self.name)

        if len(self.params):
            print('# Parameters')
        for param in self.params:
            print('%s: %i' % (param.name, param.value))

        if len(self.inputs):
            print('# Inputs')
        for input in self.inputs:
            print('%4s: %2i (%s)' % (input.name, input.size, input.type))

        if len(self.outputs):
            print('# Outputs')
        for output in self.outputs:
            print('%4s: %2i (%s)' % (output.name, output.size, output.type))

    def append_name(self, name):
        self.name = name



class Pin:
    def __init__(self, name = '', size = 1):
        self.name  = name
        self.size  = size

        if self.size > 1:
            self.type = 'bus'
        else:
            self.type = 'wire'

class Param:
    def __init__(self, name = '', value = 0):
        self.name  = name
        self.value = value