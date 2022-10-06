
from func import skip_comment


class Line:
    def __init__(self, content=''):
        self.content = content
    
    def erase_comment(self):
        self.content = skip_comment(self.content)
        return True

    # def is_name_section(self, module_name, module_body_arr, line_num):
    #     name = ''
    #     for i in range(line_num, len(module_body_arr)):
    #         line = module_body_arr[i].strip()
    #         name += line + ' '
    #         if ';' in line:
    #             name = re.sub(r'\([^()]*\)', '', name)
    #             name = name.replace('module', '')
    #             name = re.sub('[;| ]', '', name)
    #             # print(name)
    #             break
        
    #     if name == module_name:
    #         return True
    #     return False

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
