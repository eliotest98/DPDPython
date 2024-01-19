# This class represent the Variable
# A variable is formed from:
# - variable name
# - argument (optional)

class VariableObject:
    variable_name = ""
    argument = ""

    def __init__(self):
        self.variable_name = ""
        self.argument = ""

    def set_variable_name(self, variable_name):
        self.variable_name = variable_name

    def set_argument(self, argument):
        self.argument = argument

    def to_string(self):
        string_to_return = "   Variable: \n"
        string_to_return = string_to_return + "    Name: " + self.variable_name + "\n"
        if isinstance(self.argument, (str, int)):
            string_to_return = string_to_return + "    Argument: " + str(self.argument)
        else:
            string_to_return = string_to_return + "    Argument: " + self.argument.to_string()
        return string_to_return

    def abstract_syntax_tree(self):
        string_to_return = "<VARIABLE> (id," + self.variable_name + ")\n"
        if isinstance(self.argument, (str, int)):
            string_to_return = string_to_return + "<ARGUMENT> (" + str(self.argument) + ") </ARGUMENT>"
        else:
            string_to_return = string_to_return + "<ARGUMENT> (" + self.argument.abstract_syntax_tree() + ") </ARGUMENT>"
        string_to_return = string_to_return + "</VARIABLE>"
        return string_to_return
