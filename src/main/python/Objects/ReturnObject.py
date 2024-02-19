from Objects.CallFunctionObject import CallFunctionObject


# This class represent a return of a function
# A return is formed from:
# - type
# - argument
from Objects.VariableObject import VariableObject


class ReturnObject:
    argument = ""
    type = ""

    def __init__(self):
        self.type = ""
        self.argument = ""

    def set_argument(self, argument):
        self.argument = argument

    def get_argument(self):
        return self.argument

    def set_type(self, type):
        self.type = type

    def abstract_syntax_tree(self):
        return_string = "<RETURN>"
        if self.type != "":
            return_string = return_string + "<TYPE>" + self.type + "</TYPE>\n"
        if isinstance(self.argument, (CallFunctionObject, VariableObject)):
            return_string = return_string + "<ARGUMENT>" + self.argument.abstract_syntax_tree() + "</ARGUMENT>\n"
        else:
            if self.argument is None:
                return_string = return_string + "<ARGUMENT>None</ARGUMENT>\n"
            else:
                return_string = return_string + "<ARGUMENT>" + str(self.argument) + "</ARGUMENT>\n"
        return_string = return_string + "</RETURN>"
        return return_string
