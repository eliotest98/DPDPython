from Objects.CallFunctionObject import CallFunctionObject
from Objects.ReturnObject import ReturnObject
from Objects.VariableObject import VariableObject


# This class represent the function instance
# A function is formed from:
# - a name
# - parameters
# - variables
# - imports
# - instructions
# - return value
class FunctionObject:
    function_name = ""
    parameters_list = list()
    variables_list = list()
    import_list = list()
    instruction_list = list()
    return_object = ReturnObject()

    def __init__(self):
        self.function_name = ""
        self.parameters_list = list()
        self.variables_list = list()
        self.instruction_list = list()
        self.import_list = list()
        self.return_object = ReturnObject()

    def set_function_name(self, function_name):
        self.function_name = function_name

    def get_function_name(self):
        return self.function_name

    def add_parameter(self, parameter_name):
        self.parameters_list.append(parameter_name)

    def add_variable(self, variable_object):
        self.variables_list.append(variable_object)

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

    def abstract_syntax_tree(self):
        string_to_return = "<FUNCTION_DECLARATION> (id," + self.function_name + ")\n"
        if len(self.import_list) != 0:
            string_to_return = string_to_return + "<IMPORT_LIST>\n"
            for import_ in self.import_list:
                string_to_return = string_to_return + import_.abstract_syntax_tree() + "\n"
            string_to_return = string_to_return + "</IMPORT_LIST>\n"
        if len(self.parameters_list) != 0:
            string_to_return = string_to_return + "<PARAMETER_LIST>\n"
            for param in self.parameters_list:
                string_to_return = string_to_return + param.abstract_syntax_tree() + "\n"
            string_to_return = string_to_return + "</PARAMETER_LIST>\n"
        if len(self.variables_list) != 0:
            string_to_return = string_to_return + "<VARIABLE_LIST>\n"
            for variable in self.variables_list:
                string_to_return = string_to_return + variable.abstract_syntax_tree() + "\n"
            string_to_return = string_to_return + "</VARIABLE_LIST>\n"
        if len(self.instruction_list) != 0:
            string_to_return = string_to_return + "<INSTRUCTION_LIST>\n"
            for instruction in self.instruction_list:
                if isinstance(instruction, str):
                    string_to_return = string_to_return + instruction + "\n"
                else:
                    string_to_return = string_to_return + instruction.abstract_syntax_tree() + "\n"
            string_to_return = string_to_return + "</INSTRUCTION_LIST>\n"
        string_to_return = string_to_return + self.return_object.abstract_syntax_tree() + "\n"
        string_to_return = string_to_return + "</FUNCTION_DECLARATION>"
        return string_to_return
