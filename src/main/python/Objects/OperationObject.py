# This class represent an operation in a if condition
# A operation is formed from:
# - type
# - first operand
# - second operand (optional)
from Objects.CallFunctionObject import CallFunctionObject
from Objects.VariableObject import VariableObject


class OperationObject:
    operation_type = ""
    first_operand = ""
    second_operand = ""

    def __init__(self):
        self.operation_type = ""
        self.first_operand = ""
        self.second_operand = ""

    def set_operation_type(self, operation_type):
        self.operation_type = operation_type

    def get_operation_type(self):
        return self.operation_type

    def set_first_operand(self, operand):
        self.first_operand = operand

    def set_second_operand(self, operand):
        self.second_operand = operand

    def __str__(self):
        return str(self.first_operand) + " " + self.operation_type + " " + str(self.second_operand)

    def abstract_syntax_tree(self, number_of_tabs):
        string_tabs = (number_of_tabs + 1) * "\t"
        internal_string_tabs = string_tabs + "\t"
        string_to_return = "<OP>\n"
        string_to_return = string_to_return + internal_string_tabs + "<TYPE>" + str(self.operation_type) + "</TYPE>\n"
        if isinstance(self.first_operand, (VariableObject, CallFunctionObject)):
            string_to_return = string_to_return + internal_string_tabs + "<OPERAND>\n" + self.first_operand.abstract_syntax_tree(
                number_of_tabs + 2) + "\n" + internal_string_tabs + "</OPERAND>\n"
        else:
            string_to_return = string_to_return + internal_string_tabs + "<OPERAND>" + str(
                self.first_operand) + "</OPERAND>\n"
        if self.second_operand != "":
            if isinstance(self.second_operand, (VariableObject, CallFunctionObject)):
                string_to_return = string_to_return + internal_string_tabs + "<OPERAND>\n" + self.second_operand.abstract_syntax_tree(
                    number_of_tabs + 2) + "\n" + internal_string_tabs + "</OPERAND>\n"
            else:
                string_to_return = string_to_return + internal_string_tabs + "<OPERAND>" + str(self.second_operand) + "</OPERAND>\n"
        string_to_return = string_to_return + string_tabs + "</OP>\n"
        return string_to_return
