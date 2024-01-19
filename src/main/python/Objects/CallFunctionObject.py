# This class represent a call function
# A call function is formed from:
# - a path to method
# - a name method
# - a list of parameters

class CallFunctionObject:
    path = ""
    method_name = ""
    parameters_list = list()

    def __init__(self):
        self.path = ""
        self.method_name = ""
        self.parameters_list = list()

    def set_path(self, path):
        self.path = path

    def add_parameter(self, parameter):
        if parameter is None:
            self.parameters_list.append("None")
        else:
            self.parameters_list.append(parameter)

    def set_method_name(self, method_name):
        self.method_name = method_name

    def to_string(self):
        string_to_return = " Call Function:\n"
        if self.path != "":
            string_to_return = string_to_return + self.path + str(self.method_name) + "\n"
        else:
            string_to_return = string_to_return + str(self.method_name) + "\n"
        if len(self.parameters_list) != 0:
            string_to_return = string_to_return + "  Parameters: \n"
            for param in self.parameters_list:
                if isinstance(param, (str, int)):
                    string_to_return = string_to_return + str(param) + "\n"
                else:
                    string_to_return = string_to_return + param.to_string() + "\n"
        return string_to_return

    def abstract_syntax_tree(self):
        string_to_return = "<CALL_FUNCTION> (id,\n"
        if self.path != "":
            string_to_return = string_to_return + self.path + str(self.method_name) + "("
        else:
            string_to_return = string_to_return + str(self.method_name) + "("
        if len(self.parameters_list) != 0:
            for param in self.parameters_list:
                if isinstance(param, (str, int)):
                    string_to_return = string_to_return + str(param)
                else:
                    string_to_return = string_to_return + param.abstract_syntax_tree()
        string_to_return = string_to_return + ")</CALL_FUNCTION>"
        return string_to_return
