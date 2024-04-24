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

    def get_variable_name(self):
        return self.variable_name

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

    def __str__(self):
        return str(self.variable_name)

    def abstract_syntax_tree(self, number_of_tabs):
        string_tabs = (number_of_tabs + 1) * "\t"
        internal_string_tabs = string_tabs + "\t"
        string_to_return = string_tabs + "<VARIABLE>(id," + str(self.variable_name) + ")"
        if self.type != "":
            string_to_return = string_to_return + "\n" + internal_string_tabs + "<TYPE>" + self.type + "</TYPE>"
            if self.argument == "":
                string_to_return = string_to_return + "\n"
        if self.argument != "":
            if isinstance(self.argument, CallFunctionObject):
                string_to_return = string_to_return + "\n" + internal_string_tabs + "<ARGUMENT>\n" + \
                                   self.argument.abstract_syntax_tree(
                                       number_of_tabs + 1) + "\n" + internal_string_tabs + "</ARGUMENT>\n"
            elif isinstance(self.argument, VariableObject):
                string_to_return = string_to_return + "\n" + internal_string_tabs + "<ARGUMENT>\n\t" + internal_string_tabs + \
                                   self.argument.abstract_syntax_tree(
                                       -1) + "\n" + internal_string_tabs + "</ARGUMENT>\n"
            else:
                string_to_return = string_to_return + internal_string_tabs + "\n" + internal_string_tabs + "<ARGUMENT>(" + str(
                    self.argument) + ")</ARGUMENT>\n"
        string_to_return = string_to_return + string_tabs + "</VARIABLE>"
        return string_to_return
