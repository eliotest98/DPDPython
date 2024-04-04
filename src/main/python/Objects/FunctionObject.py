from Objects.CallFunctionObject import CallFunctionObject
from Objects.ReturnObject import ReturnObject

# This class represent the function instance
# A function is formed from:
# - a name
# - parameters
# - variables
# - imports
# - instructions
# - lambdas
# - rest api
# - return value
class FunctionObject:
    function_name = ""
    parameters_list = list()
    variables_list = list()
    import_list = list()
    instruction_list = list()
    lamda_list = list()
    rest_api_list = list()
    return_object = ReturnObject()

    def __init__(self):
        self.function_name = ""
        self.parameters_list = list()
        self.variables_list = list()
        self.instruction_list = list()
        self.import_list = list()
        self.lamda_list = list()
        self.rest_api_list = list()
        self.return_object = ReturnObject()

    def set_function_name(self, function_name):
        self.function_name = function_name

    def get_function_name(self):
        return self.function_name

    def add_parameter(self, parameter_name):
        self.parameters_list.append(parameter_name)

    def add_variable(self, variable_object):
        self.variables_list.append(variable_object)

    def remove_variable(self, variable_object):
        self.variables_list.remove(variable_object)

    def get_variables_list(self):
        return self.variables_list

    def add_instruction(self, instruction):
        self.instruction_list.append(instruction)

    def get_instructions_list(self):
        return self.instruction_list

    def set_return_object(self, return_object):
        self.return_object = return_object

    def get_return_object(self):
        return self.return_object

    def add_import(self, import_object):
        self.import_list.append(import_object)

    def get_imports_list(self):
        return self.import_list

    def remove_import(self, import_object):
        self.import_list.remove(import_object)

    def add_lambda_function(self, function_object):
        self.lamda_list.append(function_object)

    def add_rest_api(self, call_function_object):
        self.rest_api_list.append(call_function_object)

    def abstract_syntax_tree(self, number_of_tabs):
        string_tabs = (number_of_tabs + 1) * "\t"
        internal_string_tabs = string_tabs + "\t"
        string_to_return = string_tabs + "<FUNCTION_DECLARATION>(id," + self.function_name + ")\n"
        if len(self.rest_api_list) != 0:
            string_to_return = string_to_return + internal_string_tabs + "<REST_API>\n"
            for rest_invoke in self.rest_api_list:
                string_to_return = string_to_return + rest_invoke.abstract_syntax_tree(number_of_tabs + 2) + "\n"
            string_to_return = string_to_return + internal_string_tabs + "</REST_API>\n"
        if len(self.import_list) != 0:
            string_to_return = string_to_return + internal_string_tabs + "<IMPORT_LIST>\n"
            for import_ in self.import_list:
                string_to_return = string_to_return + import_.abstract_syntax_tree(number_of_tabs + 2) + "\n"
            string_to_return = string_to_return + internal_string_tabs + "</IMPORT_LIST>\n"
        if len(self.parameters_list) != 0:
            string_to_return = string_to_return + internal_string_tabs + "<PARAMETER_LIST>\n"
            for param in self.parameters_list:
                string_to_return = string_to_return + param.abstract_syntax_tree(number_of_tabs + 1) + "\n"
            string_to_return = string_to_return + internal_string_tabs + "</PARAMETER_LIST>\n"
        if len(self.variables_list) != 0:
            string_to_return = string_to_return + internal_string_tabs + "<VARIABLE_LIST>\n"
            for variable in self.variables_list:
                string_to_return = string_to_return + variable.abstract_syntax_tree(number_of_tabs + 2) + "\n"
            string_to_return = string_to_return + internal_string_tabs + "</VARIABLE_LIST>\n"
        if len(self.instruction_list) != 0:
            string_to_return = string_to_return + internal_string_tabs + "<INSTRUCTION_LIST>\n"
            for instruction in self.instruction_list:
                if isinstance(instruction, CallFunctionObject):
                    string_to_return = string_to_return + instruction.abstract_syntax_tree(number_of_tabs + 1) + "\n"
                else:
                    string_to_return = string_to_return + instruction.abstract_syntax_tree(number_of_tabs + 2) + "\n"
            string_to_return = string_to_return + internal_string_tabs + "</INSTRUCTION_LIST>\n"
        if len(self.lamda_list) != 0:
            string_to_return = string_to_return + internal_string_tabs + "<LAMBDA_LIST>\n"
            for instruction in self.lamda_list:
                string_to_return = string_to_return + instruction.abstract_syntax_tree(number_of_tabs + 2) + "\n"
            string_to_return = string_to_return + internal_string_tabs + "</LAMBDA_LIST>\n"
        string_to_return = string_to_return + self.return_object.abstract_syntax_tree(number_of_tabs + 1) + "\n"
        string_to_return = string_to_return + string_tabs + "</FUNCTION_DECLARATION>"
        return string_to_return
