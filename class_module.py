class Module:
    def __init__(self, name=''):
        self.name = name
        self.params = []
        self.pins = []
        # self.inputs = []
        # self.outputs = []
        # self.inouts = []

    def print(self):
        if self.name == '':
            print('Not found')
            return
        else:
            print('Module: ' + self.name)

        print("Parameters [%i]:" % len(self.pins))
        for param in self.params:
            print('%s = %i' % (param.name, param.value))
        print('')

        print("Pins [%i]:" % len(self.pins))
        for pin in self.pins:
            if pin.direction == 'input':
                print('%7s %8s: %2i (%s)' % (pin.direction, pin.name, pin.size, pin.type))
        print('')

        for pin in self.pins:
            if pin.direction == 'output':
                print('%7s %8s: %2i (%s)' % (pin.direction, pin.name, pin.size, pin.type))
        print('')

        for pin in self.pins:
            if pin.direction == 'inout':
                print('%7s %8s: %2i (%s)' % (pin.direction, pin.name, pin.size, pin.type))
        print('')

    def append_name(self, name):
        self.name = name

    def append_params(self, param):
        self.params.append(param)

    def append_pin(self, pin):
        if pin.direction == 'input':
            self.pins.append(pin)
        elif pin.direction == 'output':
            self.pins.append(pin)
        elif pin.direction == 'inout':
            self.pins.append(pin)
        else:
            print('fatal: wrong type of pin %s' % pin.name)


class Module_for_search():
    def __init__(self, name=''):
        self.name = name
        self.attachments = []
        self.called = False
        self.count_att = 0



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
