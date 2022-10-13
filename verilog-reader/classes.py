from func import *

class Module:
    def __init__(self, name=''):
        self.name = name
        self.pins = []

    def print(self, file):
        if self.name == '':
            print('fatal: empty module\n')
            exit()

        file.write('Name: %s\n' % self.name)

        file.write("Pins [%i]:\n" % len(self.pins))
        for pin in self.pins:
            for dir in ['input', 'output', 'inout']:
                if dir == pin.direction:
                    file.write('%7s %12s %6s\n' % (pin.direction, pin.name, pin.wire_type))

    def append_name(self, name):
        self.name = name

    def append_pin(self, pin):
        if pin.direction == 'input' or \
            pin.direction == 'output' or \
            pin.direction == 'inout':
            self.pins.append(pin)
        else:
            print('fatal: wrong type of pin %s\n' % pin.name)
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
        self.wire_type = wire_type


class Line:
    def __init__(self, content=''):
        self.content = content
    
    def erase_comment(self):
        self.content = skip_comment(self.content)
        return True

    def is_pin_section(self):
        if 'input' in self.content or 'output' in self.content or 'inout' in self.content:
            return True
        return False

    def is_endmodule_section(self):
        if 'endmodule' in self.content:
            return True
        return False

    def is_module_section(self):
        if 'module' in self.content and not 'endmodule' in self.content:
            return True
        return False
