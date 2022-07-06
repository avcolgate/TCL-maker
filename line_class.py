import re

class Line:
    def __init__(self, content = ''):
        self.content = content
    
    def is_comment(self):
        if re.sub("[ |\t]","", self.content).find('//') == 0:
            return True
        return False

    def is_name_section(self, name):
        if 'module' in self.content and str(name) in self.content:
            return True
        return False

    def is_param_section(self):
        if 'parameter' in self.content:
            return True
        return False

    def is_pin_section(self):
        if 'input' in self.content or 'output' in self.content:
            return True
        return False

    def is_endmodule_section(self):
        if 'endmodule' in self.content:
            return True
        return False

