class Module:
    def __init__(self, name=''):
        self.name = name
        self.params = []
        self.inputs = []
        self.outputs = []
        self.inouts = []
        self.called = False

    def print(self):
        if self.name == '':
            print('Not found')
            return
        else:
            print(self.name)

        # if len(self.params):
        #     print('# Parameters')
        # for param in self.params:
        #     print('%s: %i' % (param.name, param.value))

        if len(self.inputs):
            print('# Inputs [%i]' % len(self.inputs))
        for pin in self.inputs:
            print('%8s: %2i (%s)' % (pin.name, pin.size, pin.type))

        if len(self.outputs):
            print('# Outputs [%i]' % len(self.outputs))
        for pin in self.outputs:
            print('%8s: %2i (%s)' % (pin.name, pin.size, pin.type))

        if len(self.inouts):
            print('# Inouts [%i]' % len(self.inouts))
        for pin in self.inouts:
            print('%8s: %2i (%s)' % (pin.name, pin.size, pin.type))

    def append_name(self, name):
        self.name = name

    def append_params(self, param):
        self.params.append(param)

    def append_pin(self, pin):
        if pin.direction == 'input':
            self.inputs.append(pin)
        elif pin.direction == 'output':
            self.outputs.append(pin)
        elif pin.direction == 'inout':
            self.inouts.append(pin)
        else:
            print('fatal: wrong type of pin %s' % pin.name)


class Pin:
    def __init__(self, name='', direction='', size=1):
        self.name = name
        self.direction = direction
        self.size = size

        if self.size > 1:
            self.type = 'bus'
        else:
            self.type = 'wire'


class Param:
    def __init__(self, name='', value=0):
        self.name = name
        self.value = value
