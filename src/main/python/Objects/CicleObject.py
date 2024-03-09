from Objects.VariableObject import VariableObject


# This class represent a cicle
# A cicle is formed from:
# - a condition
# - a list of instructions of body
class CicleObject:
    condition = ""
    instructions_list = list()

    def __init__(self):
        self.condition = ""
        self.instructions_list = list()

    def set_condition(self, condition):
        self.condition = condition

    def add_instruction(self, instruction):
        self.instructions_list.append(instruction)

    def abstract_syntax_tree(self, number_of_tabs):
        string_tabs = (number_of_tabs + 1) * "\t"
        internal_string_tabs = string_tabs + "\t"
        string_to_return = string_tabs + "<CICLE>\n"
        string_to_return = string_to_return + internal_string_tabs + "<CONDITION>\n"
        if isinstance(self.condition, VariableObject):
            string_to_return = string_to_return + self.condition.abstract_syntax_tree(number_of_tabs + 2)
        else:
            string_to_return = string_to_return + self.condition.abstract_syntax_tree(number_of_tabs + 1)
        string_to_return = string_to_return + "\n" + internal_string_tabs + "</CONDITION>\n"
        if len(self.instructions_list) != 0:
            string_to_return = string_to_return + internal_string_tabs + "<INSTRUCTION_LIST>\n"
            for instruction in self.instructions_list:
                string_to_return = string_to_return + instruction.abstract_syntax_tree(number_of_tabs + 2) + "\n"
            string_to_return = string_to_return + internal_string_tabs + "</INSTRUCTION_LIST>\n"
        string_to_return = string_to_return + string_tabs + "</CICLE>"
        return string_to_return
