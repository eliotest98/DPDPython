from Objects.CallFunctionObject import CallFunctionObject
from Objects.VariableObject import VariableObject


# This class represent the function instance
# A function is formed from:
# - a name
# - parameters (optionals)
# - variables (optionals)
# - instructions
# - return value (optionals)
class FunctionObject:
    function_name = ""
    parameters_list = list()
    variables_list = list()
    instruction_list = list()
    return_value = ""

    def __init__(self):
        self.function_name = ""
        self.parameters_list = list()
        self.variables_list = list()
        self.instruction_list = list()
        self.return_value = ""

    def set_function_name(self, function_name):
        self.function_name = function_name

    def add_parameter(self, parameter_name):
        self.parameters_list.append(parameter_name)

    def add_variable(self, variable_object):
        self.variables_list.append(variable_object)

    def add_instruction(self, instruction):
        self.instruction_list.append(instruction)

    def set_return_value(self, return_value_object):
        if return_value_object is None:
            self.return_value = "None"
        else:
            self.return_value = return_value_object

    def to_string(self):
        string_to_return = "  Function Name: " + self.function_name + "\n"
        if len(self.parameters_list) != 0:
            string_to_return = string_to_return + "  Parameters: \n"
            for param in self.parameters_list:
                string_to_return = string_to_return + param.to_string() + "\n"
        if len(self.variables_list) != 0:
            string_to_return = string_to_return + "  Variables: \n"
            for variable in self.variables_list:
                string_to_return = string_to_return + variable.to_string() + "\n"
        if len(self.instruction_list) != 0:
            string_to_return = string_to_return + "Instructions: \n"
            for instruction in self.instruction_list:
                if isinstance(instruction, str):
                    string_to_return = string_to_return + instruction + "\n"
                else:
                    string_to_return = string_to_return + instruction.to_string() + "\n"
        if isinstance(self.return_value, (VariableObject, CallFunctionObject)):
            string_to_return = string_to_return + "   Return Value: \n"
            string_to_return = string_to_return + self.return_value.to_string() + "\n"
        else:
            string_to_return = string_to_return + "   Return Value: " + self.return_value
        return string_to_return

    def abstract_syntax_tree(self):
        string_to_return = "<FUNCTION_DECLARATION> (id," + self.function_name + ")\n"
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
        if isinstance(self.return_value, (VariableObject, CallFunctionObject)):
            string_to_return = string_to_return + "<RETURN>"
            string_to_return = string_to_return + self.return_value.abstract_syntax_tree() + "\n"
            string_to_return = string_to_return + "</RETURN>"
        else:
            string_to_return = string_to_return + "<RETURN>"
            string_to_return = string_to_return + self.return_value
            string_to_return = string_to_return + "</RETURN>"
        string_to_return = string_to_return + "</FUNCTION_DECLARATION>"
        return string_to_return
