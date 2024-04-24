# This class represent a call function
# A call function is formed from:
# - a path to method
# - a name method
# - a list of parameters
# - the origin class name who implement the function called
from bytecode import CellVar, FreeVar


class CallFunctionObject:
    path = ""
    method_name = ""
    parameters_list = list()
    concatenation_calls = list()
    origin_class_name = ""

    def __init__(self):
        self.path = ""
        self.method_name = ""
        self.parameters_list = list()
        self.concatenation_calls = list()
        self.origin_class_name = ""

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def add_parameter(self, parameter):
        if parameter is None:
            self.parameters_list.append("None")
        else:
            self.parameters_list.append(parameter)

    def get_parameters_list(self):
        return self.parameters_list

    def add_concat(self, call_function_object):
        self.concatenation_calls.append(call_function_object)

    def set_method_name(self, method_name):
        self.method_name = method_name

    def get_method_name(self):
        return self.method_name

    def set_original_class_name(self, origin_class_name):
        self.origin_class_name = origin_class_name

    def get_original_class_name(self):
        return self.origin_class_name

    def __str__(self):
        params = "("
        for parameter in self.parameters_list:
            params = params + str(parameter) + " , "
        params = params.removesuffix(" , ") + ")"
        return str(self.path) + str(self.method_name) + str(params)

    def abstract_syntax_tree(self, number_of_tabs):
        string_tabs = (number_of_tabs + 2) * "\t"
        internal_string_tabs = string_tabs + "\t"
        string_to_return = ""
        if len(self.concatenation_calls) != 0:
            string_to_return = string_tabs + "<CONCATENATE_FUNCTION>"
            for call in self.concatenation_calls:
                if isinstance(call, str):
                    string_to_return = string_to_return + "\n" + internal_string_tabs + call
                else:
                    string_to_return = string_to_return + "\n" + call.abstract_syntax_tree(number_of_tabs + 1)
            string_to_return = string_to_return + internal_string_tabs + "\n" + internal_string_tabs + "<CALL_FUNCTION> (id,\n"
            if self.path != "":
                string_to_return = string_to_return + self.path + str(self.method_name) + "("
            else:
                string_to_return = string_to_return + internal_string_tabs + "\t" + str(self.method_name) + "("
            if len(self.parameters_list) != 0:
                self.parameters_list.reverse()
                for param in self.parameters_list:
                    if isinstance(param, (str, int, tuple)):
                        string_to_return = string_to_return + str(param) + ","
                    else:
                        string_to_return = string_to_return + "\n" + param.abstract_syntax_tree(
                            number_of_tabs + 2) + ","
                string_to_return = string_to_return.removesuffix(",")
            string_to_return = string_to_return + ")\n" + internal_string_tabs + "</CALL_FUNCTION>\n"
            string_to_return = string_to_return + string_tabs + "</CONCATENATE_FUNCTION>"
            return string_to_return
        string_to_return = string_to_return + string_tabs + "<CALL_FUNCTION>(id,\n"
        if self.path != "":
            string_to_return = string_to_return + internal_string_tabs + self.path + str(self.method_name) + "("
        else:
            string_to_return = string_to_return + internal_string_tabs + str(self.method_name) + "("
        if len(self.parameters_list) != 0:
            self.parameters_list.reverse()
            for param in self.parameters_list:
                if isinstance(param, (str, int, tuple, float, CellVar, FreeVar, bytes, frozenset, complex, list)):
                    string_to_return = string_to_return + str(param) + "\n\t" + internal_string_tabs + ","
                elif isinstance(param, CallFunctionObject):
                    string_to_return = string_to_return + "\n" + param.abstract_syntax_tree(
                        number_of_tabs + 2) + "\n\t" + internal_string_tabs + ","
                else:
                    string_to_return = string_to_return + "\n" + internal_string_tabs + param.abstract_syntax_tree(
                        number_of_tabs + 2) + internal_string_tabs + ","
            string_to_return = string_to_return.removesuffix(",")
        string_to_return = string_to_return + "))"
        if self.origin_class_name != "":
            string_to_return = string_to_return + "\n" + internal_string_tabs + "<ORIGIN_CLASS_NAME>" + \
                               self.origin_class_name + "</ORIGIN_CLASS_NAME>"
        string_to_return = string_to_return + "\n" + string_tabs + "</CALL_FUNCTION>"
        return string_to_return
