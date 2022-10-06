
class Module:
    def __init__(self, name=''):
        self.name = name
        self.pins = []

    def print(self):
        
        print('Name: %s\n' % self.name)

        print("Pins [%i]:" % len(self.pins))
        for pin in self.pins:
            for dir in ['input', 'output', 'inout']:
                if dir == pin.direction:
                    print('%7s %12s %6s' % (pin.direction, pin.name, pin.is_bus))
        print('\n')

    def append_name(self, name):
        self.name = name

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
    def __init__(self, name='', direction='', wire_type='wire'):
        self.name = name
        self.direction = direction
        self.is_bus = wire_type
