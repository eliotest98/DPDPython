# This class represent a call function
# A call function is formed from:
# - a path to method
# - a name method
# - a list of parameters

class CallFunctionObject:
    path = ""
    method_name = ""
    parameters_list = list()
    concatenation_calls = list()

    def __init__(self):
        self.path = ""
        self.method_name = ""
        self.parameters_list = list()
        self.concatenation_calls = list()

    def set_path(self, path):
        self.path = path

    def add_parameter(self, parameter):
        if parameter is None:
            self.parameters_list.append("None")
        else:
            self.parameters_list.append(parameter)

    def add_concat(self, call_function_object):
        self.concatenation_calls.append(call_function_object)

    def set_method_name(self, method_name):
        self.method_name = method_name

    def abstract_syntax_tree(self):
        string_to_return = ""
        if len(self.concatenation_calls) != 0:
            string_to_return = "<CONCATENATE_FUNCTION>"
            for call in self.concatenation_calls:
                string_to_return = string_to_return + call.abstract_syntax_tree()
            string_to_return = string_to_return + "<CALL_FUNCTION> (id,\n"
            if self.path != "":
                string_to_return = string_to_return + self.path + str(self.method_name) + "("
            else:
                string_to_return = string_to_return + str(self.method_name) + "("
            if len(self.parameters_list) != 0:
                self.parameters_list.reverse()
                for param in self.parameters_list:
                    if isinstance(param, (str, int, tuple)):
                        string_to_return = string_to_return + str(param) + ","
                    else:
                        string_to_return = string_to_return + param.abstract_syntax_tree() + ","
                string_to_return = string_to_return.removesuffix(",")
            string_to_return = string_to_return + ")</CALL_FUNCTION>"
            string_to_return = string_to_return + "</CONCATENATE_FUNCTION>"
            return string_to_return
        string_to_return = string_to_return + "<CALL_FUNCTION> (id,\n"
        if self.path != "":
            string_to_return = string_to_return + self.path + str(self.method_name) + "("
        else:
            string_to_return = string_to_return + str(self.method_name) + "("
        if len(self.parameters_list) != 0:
            self.parameters_list.reverse()
            for param in self.parameters_list:
                if isinstance(param, (str, int, tuple)):
                    string_to_return = string_to_return + str(param) + ","
                else:
                    string_to_return = string_to_return + param.abstract_syntax_tree() + ","
            string_to_return = string_to_return.removesuffix(",")
        string_to_return = string_to_return + ")</CALL_FUNCTION>"
        return string_to_return
