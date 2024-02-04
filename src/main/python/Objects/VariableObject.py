# This class represent the Variable
# A variable is formed from:
# - variable name
# - argument (optional)
from Objects.CallFunctionObject import CallFunctionObject


class VariableObject:
    variable_name = ""
    argument = ""

    def __init__(self):
        self.variable_name = ""
        self.argument = ""

    def set_variable_name(self, variable_name):
        self.variable_name = variable_name

    def set_argument(self, argument):
        if argument is None:
            self.argument = "None"
        else:
            self.argument = argument

    def abstract_syntax_tree(self):
        string_to_return = "<VARIABLE> (id," + self.variable_name + ")\n"
        if self.argument != "":
            if isinstance(self.argument, (VariableObject, CallFunctionObject)):
                string_to_return = string_to_return + "<ARGUMENT> (" + self.argument.abstract_syntax_tree() + ") </ARGUMENT>"
            else:
                string_to_return = string_to_return + "<ARGUMENT> (" + str(self.argument) + ") </ARGUMENT>"
        string_to_return = string_to_return + "</VARIABLE>"
        return string_to_return
