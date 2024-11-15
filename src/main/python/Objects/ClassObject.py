from Objects.CallFunctionObject import CallFunctionObject
from Objects.FunctionObject import FunctionObject


# This class represent the class instance
# A class is formed from:
# - the name of file where the class is created
# - a name
# - a list of superclass
# - a list of imports
# - a constructor with "__init__" key
# - some functions with "def" key
# - variables
# - instructions
from Objects.IfObject import IfObject
from Objects.VariableObject import VariableObject


class ClassObject:
    class_name = ""
    file_name = ""
    functions_list = list()
    constructor = FunctionObject()
    variables_list = list()
    import_list = list()
    instructions_list = list()
    superclass_list = list()

    def __init__(self):
        self.class_name = ""
        self.file_name = ""
        self.functions_list = list()
        self.constructor = FunctionObject()
        self.variables_list = list()
        self.import_list = list()
        self.instructions_list = list()
        self.superclass_list = list()

    def set_class_name(self, class_name):
        self.class_name = class_name

    def get_class_name(self):
        return self.class_name

    def add_function(self, function_object):
        self.functions_list.append(function_object)

    def remove_function(self, function_object):
        self.functions_list.remove(function_object)

    def get_functions_list(self):
        return self.functions_list

    def set_constructor(self, function_object):
        self.constructor = function_object

    def get_constructor(self):
        return self.constructor

    def add_variable(self, variable_object):
        self.variables_list.append(variable_object)

    def remove_variable(self, variable_object):
        self.variables_list.remove(variable_object)

    def get_variables_list(self):
        return self.variables_list

    def add_import(self, import_object):
        self.import_list.append(import_object)

    def get_imports_list(self):
        return self.import_list

    def add_instruction(self, instruction):
        self.instructions_list.append(instruction)

    def get_instructions_list(self):
        return self.instructions_list

    def add_superclass(self, superclass_name):
        if superclass_name not in self.superclass_list:
            self.superclass_list.append(superclass_name)

    def get_superclass_list(self):
        return self.superclass_list

    def remove_superclass(self, superclass_name):
        self.superclass_list.remove(superclass_name)

    def set_file_name(self, file_name):
        self.file_name = file_name

    def get_file_name(self):
        return self.file_name

    def abstract_syntax_tree(self, number_of_tabs):
        string_tabs = (number_of_tabs + 1) * "\t"
        internal_string_tabs = string_tabs + "\t"
        string_to_return = string_tabs + "<CLASS>(id," + self.class_name + ")\n"
        if len(self.superclass_list) != 0:
            string_to_return = string_to_return + internal_string_tabs + "<SUPERCLASS_LIST>\n"
            for superclass in self.superclass_list:
                string_to_return = string_to_return + internal_string_tabs + "\t<SUPERCLASS>" + superclass + "</SUPERCLASS>\n"
            string_to_return = string_to_return + internal_string_tabs + "</SUPERCLASS_LIST>\n"
        if len(self.import_list) != 0:
            string_to_return = string_to_return + internal_string_tabs + "<IMPORT_LIST>\n"
            for import_ in self.import_list:
                string_to_return = string_to_return + import_.abstract_syntax_tree(number_of_tabs + 2) + "\n"
            string_to_return = string_to_return + internal_string_tabs + "</IMPORT_LIST>\n"
        if len(self.variables_list) != 0:
            string_to_return = string_to_return + internal_string_tabs + "<VARIABLE_LIST>\n"
            for variable in self.variables_list:
                string_to_return = string_to_return + variable.abstract_syntax_tree(number_of_tabs + 2) + "\n"
            string_to_return = string_to_return + internal_string_tabs + "</VARIABLE_LIST>\n"
        if self.constructor.function_name != "":
            string_to_return = string_to_return + internal_string_tabs + "<CONSTRUCTOR_DECLARATION>\n"
            string_to_return = string_to_return + self.constructor.abstract_syntax_tree(number_of_tabs + 2) + "\n"
            string_to_return = string_to_return + internal_string_tabs + "</CONSTRUCTOR_DECLARATION>\n"
        if len(self.functions_list) != 0:
            string_to_return = string_to_return + internal_string_tabs + "<FUNCTION_LIST>\n"
            for function in self.functions_list:
                string_to_return = string_to_return + function.abstract_syntax_tree(number_of_tabs + 2) + "\n"
            string_to_return = string_to_return + internal_string_tabs + "</FUNCTION_LIST>\n"
        if len(self.instructions_list) != 0:
            string_to_return = string_to_return + internal_string_tabs + "<INSTRUCTION_LIST>\n"
            for instruction in self.instructions_list:
                if isinstance(instruction, CallFunctionObject):
                    string_to_return = string_to_return + instruction.abstract_syntax_tree(number_of_tabs + 1) + "\n"
                else:
                    string_to_return = string_to_return + instruction.abstract_syntax_tree(number_of_tabs + 2) + "\n"
            string_to_return = string_to_return + internal_string_tabs + "</INSTRUCTION_LIST>\n"
        string_to_return = string_to_return + string_tabs + "</CLASS>"
        return string_to_return

    def has_field_type(self, field_type):
        for variable in self.variables_list:
            if variable.get_type() == field_type:
                return True
        return False

    def get_field(self, fio):
        for fo in self.variables_list:
            if fo.get_type() == fio.get_original_class_name():
                return fo
        return None
