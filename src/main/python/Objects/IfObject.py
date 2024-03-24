from Objects.CallFunctionObject import CallFunctionObject
from Objects.ExceptionObject import ExceptionObject
from Objects.OperationObject import OperationObject
from Objects.VariableObject import VariableObject


# This class represent an If
# An If condition is formed from:
# - operation
# - instructions list if true
# - instruction list if false
# - inverse for not operation
class IfObject:
    operation_object = OperationObject()
    instruction_list_if_true = list()
    instruction_list_if_false = list()
    inverse = False

    def __init__(self):
        self.instruction_list_if_true = list()
        self.instruction_list_if_false = list()
        self.operation_object = OperationObject()

    def set_operation(self, operation_object):
        self.operation_object = operation_object

    def add_instruction_true(self, instruction):
        self.instruction_list_if_true.append(instruction)

    def get_instruction_list_true(self):
        return self.instruction_list_if_true

    def add_instruction_false(self, instruction):
        self.instruction_list_if_false.append(instruction)

    def get_instruction_list_false(self):
        return self.instruction_list_if_false

    def is_inverse(self):
        return self.inverse

    def set_inverse(self, inverse):
        self.inverse = inverse
        if isinstance(self.operation_object, OperationObject):
            self.operation_object.set_operation_type("NOT")

    def abstract_syntax_tree(self, number_of_tabs):
        string_tabs = (number_of_tabs + 1) * "\t"
        internal_string_tabs = string_tabs + "\t"
        if isinstance(self.operation_object, (VariableObject, CallFunctionObject)):
            string_to_return = string_tabs + "<IF>\n"
            string_to_return = string_to_return + internal_string_tabs + self.operation_object.abstract_syntax_tree(
                number_of_tabs + 1)
            if len(self.instruction_list_if_true) != 0:
                string_to_return = string_to_return + internal_string_tabs + "<INSTRUCTION_LIST_IF_TRUE>\n"
                for instruction in self.instruction_list_if_true:
                    if isinstance(instruction, CallFunctionObject):
                        string_to_return = string_to_return + instruction.abstract_syntax_tree(
                            number_of_tabs + 1) + "\n"
                    else:
                        string_to_return = string_to_return + instruction.abstract_syntax_tree(
                            number_of_tabs + 2) + "\n"
                string_to_return = string_to_return + internal_string_tabs + "</INSTRUCTION_LIST_IF_TRUE>\n"
            if len(self.instruction_list_if_false) != 0:
                string_to_return = string_to_return + internal_string_tabs + "<INSTRUCTION_LIST_IF_FALSE>\n"
                for instruction in self.instruction_list_if_false:
                    if isinstance(instruction, CallFunctionObject):
                        string_to_return = string_to_return + instruction.abstract_syntax_tree(
                            number_of_tabs + 1) + "\n"
                    else:
                        string_to_return = string_to_return + instruction.abstract_syntax_tree(
                            number_of_tabs + 2) + "\n"
                string_to_return = string_to_return + internal_string_tabs + "</INSTRUCTION_LIST_IF_FALSE>\n"
            string_to_return = string_to_return + string_tabs + "</IF>"
        elif self.operation_object.get_operation_type() != "":
            string_to_return = string_tabs + "<IF>\n"
            string_to_return = string_to_return + internal_string_tabs + self.operation_object.abstract_syntax_tree(
                number_of_tabs + 1)
            if len(self.instruction_list_if_true) != 0:
                string_to_return = string_to_return + internal_string_tabs + "<INSTRUCTION_LIST_IF_TRUE>\n"
                for instruction in self.instruction_list_if_true:
                    if isinstance(instruction, CallFunctionObject):
                        string_to_return = string_to_return + instruction.abstract_syntax_tree(
                            number_of_tabs + 1) + "\n"
                    else:
                        string_to_return = string_to_return + instruction.abstract_syntax_tree(
                            number_of_tabs + 2) + "\n"
                string_to_return = string_to_return + internal_string_tabs + "</INSTRUCTION_LIST_IF_TRUE>\n"
            if len(self.instruction_list_if_false) != 0:
                string_to_return = string_to_return + internal_string_tabs + "<INSTRUCTION_LIST_IF_FALSE>\n"
                for instruction in self.instruction_list_if_false:
                    if isinstance(instruction, CallFunctionObject):
                        string_to_return = string_to_return + instruction.abstract_syntax_tree(
                            number_of_tabs + 1) + "\n"
                    else:
                        string_to_return = string_to_return + instruction.abstract_syntax_tree(
                            number_of_tabs + 2) + "\n"
                string_to_return = string_to_return + internal_string_tabs + "</INSTRUCTION_LIST_IF_FALSE>\n"
            string_to_return = string_to_return + string_tabs + "</IF>"
        else:
            string_to_return = string_tabs + "<ELSE>\n"
            if len(self.instruction_list_if_true) != 0:
                string_to_return = string_to_return + internal_string_tabs + "<INSTRUCTION_LIST>\n"
                for instruction in self.instruction_list_if_true:
                    if isinstance(instruction, VariableObject):
                        string_to_return = string_to_return + instruction.abstract_syntax_tree(number_of_tabs + 2)
                    elif isinstance(instruction, CallFunctionObject):
                        string_to_return = string_to_return + instruction.abstract_syntax_tree(
                            number_of_tabs + 1) + "\n"
                    else:
                        string_to_return = string_to_return + instruction.abstract_syntax_tree(number_of_tabs + 1)
                string_to_return = string_to_return + "\n" + internal_string_tabs + "</INSTRUCTION_LIST>\n"
            string_to_return = string_to_return + string_tabs + "</ELSE>"
        return string_to_return
