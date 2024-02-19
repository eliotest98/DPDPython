from Objects.CallFunctionObject import CallFunctionObject


# This class represent the Variable
# A variable is formed from:
# - variable name
# - argument
# - type
class VariableObject:
    type = ""
    variable_name = ""
    argument = ""

    def __init__(self):
        self.variable_name = ""
        self.argument = ""
        self.type = ""

    def set_variable_name(self, variable_name):
        self.variable_name = variable_name

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def set_argument(self, argument):
        if argument is None:
            self.argument = "None"
        else:
            self.argument = argument

    def get_argument(self):
        return self.argument

    def abstract_syntax_tree(self):
        string_to_return = "<VARIABLE> (id," + self.variable_name + ")\n"
        if self.type != "":
            string_to_return = string_to_return + "<TYPE>" + self.type + "</TYPE>\n"
        if self.argument != "":
            if isinstance(self.argument, (VariableObject, CallFunctionObject)):
                string_to_return = string_to_return + "<ARGUMENT> (" + self.argument.abstract_syntax_tree() + ") </ARGUMENT>\n"
            else:
                string_to_return = string_to_return + "<ARGUMENT> (" + str(self.argument) + ") </ARGUMENT>\n"
        string_to_return = string_to_return + "</VARIABLE>"
        return string_to_return
