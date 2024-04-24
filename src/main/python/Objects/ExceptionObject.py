# This class represent the try except statement
# A try except is formed from:
# - instructions for try clause
# - instructions for except clause
from bytecode import FreeVar, CellVar


class ExceptionObject:
    instruction_list_try = list()
    instruction_list_except = dict()

    def __init__(self):
        self.instruction_list_try = list()
        self.instruction_list_except = dict()

    def add_instruction_try(self, instruction):
        self.instruction_list_try.append(instruction)

    def get_instruction_list_try(self):
        return self.instruction_list_try

    def add_instruction_except(self, except_name, instruction):
        if isinstance(except_name, (FreeVar, CellVar)):
            return
        if except_name not in self.instruction_list_except:
            self.instruction_list_except[except_name] = list()
        self.instruction_list_except[except_name].append(instruction)

    def get_instruction_list_except(self):
        return self.instruction_list_except

    def abstract_syntax_tree(self, number_of_tabs):
        string_tabs = (number_of_tabs + 1) * "\t"
        internal_string_tabs = string_tabs + "\t"
        instruction_tab = internal_string_tabs + "\t"
        string_to_return = string_tabs + "<EXCEPTION>\n"
        string_to_return = string_to_return + internal_string_tabs + "<TRY>\n"
        if len(self.instruction_list_try) != 0:
            string_to_return = string_to_return + instruction_tab + "<INSTRUCTION_LIST>\n"
            for instruction in self.instruction_list_try:
                string_to_return = string_to_return + instruction.abstract_syntax_tree(number_of_tabs + 3) + "\n"
            string_to_return = string_to_return + instruction_tab + "</INSTRUCTION_LIST>\n"
        string_to_return = string_to_return + internal_string_tabs + "</TRY>\n"
        if len(self.instruction_list_except) != 0:
            for key in self.instruction_list_except:
                string_to_return = string_to_return + internal_string_tabs + "<EXCEPT> (id," + str(key) + ")\n"
                if len(self.instruction_list_except[key]) != 0:
                    string_to_return = string_to_return + instruction_tab + "<INSTRUCTION_LIST>\n"
                    for instruction in self.instruction_list_except[key]:
                        string_to_return = string_to_return + instruction.abstract_syntax_tree(
                            number_of_tabs + 3) + "\n"
                    string_to_return = string_to_return + instruction_tab + "</INSTRUCTION_LIST>\n"
                string_to_return = string_to_return + internal_string_tabs + "</EXCEPT>\n"
        string_to_return = string_to_return + string_tabs + "</EXCEPTION>"
        return string_to_return
