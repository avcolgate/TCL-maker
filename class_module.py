
class Module:
    def __init__(self, name=''):
        self.name = name
        self.params = []
        self.defines = []
        self.pins = []

    def print(self):
        
        print('Name: %s\n' % self.name)

        print("Defines [%i]:" % len(self.defines))
        for define in self.defines:
            print('%10s = %i' % (define.name, define.value))
        print('')

        print("Parameters [%i]:" % len(self.params))
        for param in self.params:
            print('%10s = %i' % (param.name, param.value))
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

    def append_param(self, param):
        self.params.append(param)

    def append_defines(self, define):
        self.defines.append(define)

    def append_pin(self, pin):
        if pin.direction == 'input' or \
            pin.direction == 'output' or \
            pin.direction == 'inout':
            self.pins.append(pin)
        else:
            print('fatal: wrong type of pin %s' % pin.name)
            exit()


class Module_for_search():
    def __init__(self, name=''):
        self.name = name
        self.attachments = []
        self.called = False
        self.attach_num = 0
        self.offset = 0
        self.text = ''
        self.text_arr = []



class Pin:
    def __init__(self, name='', direction='', size=-1):
        self.name = name
        self.direction = direction
        self.size = size

        if self.size > 1:
            self.type = 'bus'
        else:
            self.type = 'wire'


class Parameter:
    def __init__(self, name='', value=-1):
        self.name = name
        self.value = value

class Define:
    def __init__(self, name='', value=-1):
        self.name = name
        self.value = value
