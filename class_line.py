import re


class Line:
    def __init__(self, content=''):
        self.content = content
    
    def erase_comment(self):
        if '//' in self.content:
            self.content = self.content[:self.content.find('//')]
        return True

    def is_name_section(self, module_name, module_body, line_num):
        name = ''
        for i in range(line_num, len(module_body)):
            line = module_body[i].strip()
            name += line + ' '
            if ';' in line:
                name = re.sub(r'\([^()]*\)', '', name)
                name = name.replace('module', '')
                name = re.sub('[;| ]', '', name)
                # print(name)
                break
        
        if name == module_name:
            return True
        return False

    def is_param_section(self):
        if 'parameter' in self.content:
            return True
        return False

    def is_pin_section(self):
        if 'input' in self.content or 'output' in self.content or 'inout' in self.content:
            return True
        return False

    def is_endmodule_section(self):
        if 'endmodule' in self.content:
            return True
        return False
