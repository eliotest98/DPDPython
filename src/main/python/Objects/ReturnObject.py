from Objects.CallFunctionObject import CallFunctionObject
from Objects.VariableObject import VariableObject

# This class represent a return of a function
# A return is formed from:
# - type
# - argument
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

    def is_empty(self):
        if self.type == "" and self.argument == "":
            return True
        else:
            return False

    def abstract_syntax_tree(self, number_of_tabs):
        string_tabs = (number_of_tabs + 1) * "\t"
        internal_string_tabs = string_tabs + "\t"
        return_string = string_tabs + "<RETURN>\n"
        if self.type != "":
            return_string = return_string + internal_string_tabs + "<TYPE>" + self.type + "</TYPE>\n"
        if isinstance(self.argument, CallFunctionObject):
            return_string = return_string + internal_string_tabs + "<ARGUMENT>\n" + self.argument.abstract_syntax_tree(
                number_of_tabs + 1) + internal_string_tabs + "\n" + internal_string_tabs + "</ARGUMENT>\n"
        elif isinstance(self.argument, VariableObject):
            return_string = return_string + internal_string_tabs + "<ARGUMENT>\n" + internal_string_tabs \
                            + "\t" + self.argument.abstract_syntax_tree(-1) + internal_string_tabs + \
                            "\n" + internal_string_tabs + "</ARGUMENT>\n"
        else:
            if self.argument is None:
                return_string = return_string + internal_string_tabs + "<ARGUMENT>None</ARGUMENT>\n"
            else:
                return_string = return_string + internal_string_tabs + "<ARGUMENT>" + str(
                    self.argument) + "</ARGUMENT>\n"
        return_string = return_string + string_tabs + "</RETURN>"
        return return_string
