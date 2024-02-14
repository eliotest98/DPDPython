from Objects.FunctionObject import FunctionObject


# This class represent the class instance
# A class is formed from:
# - a name
# - a list of superclass
# - a list of imports
# - a constructor with "__init__" key
# - some functions with "def" key
# - variables
# - instructions
class ClassObject:
    class_name = ""
    superclass_list = list()
    import_list = list()
    functions_list = list()
    constructor = FunctionObject()
    variables_list = list()
    instructions_list = list()

    def __init__(self):
        self.class_name = ""
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

    def get_functions_list(self):
        return self.functions_list

    def set_constructor(self, function_object):
        self.constructor = function_object

    def add_variable(self, variable_object):
        self.variables_list.append(variable_object)

    def add_import(self, import_object):
        self.import_list.append(import_object)

    def add_instruction(self, instruction):
        self.instructions_list.append(instruction)

    def add_superclass(self, superclass_name):
        self.superclass_list.append(superclass_name)

    def abstract_syntax_tree(self):
        string_to_return = "<CLASS> (id," + self.class_name + ")\n"
        if len(self.superclass_list) != 0:
            string_to_return = string_to_return + "<SUPERCLASS_LIST>\n"
            for superclass in self.superclass_list:
                string_to_return = string_to_return + "<SUPERCLASS>" + superclass + "</SUPERCLASS>\n"
            string_to_return = string_to_return + "</SUPERCLASS_LIST>\n"
        if len(self.import_list) != 0:
            string_to_return = string_to_return + "<IMPORT_LIST>\n"
            for import_ in self.import_list:
                string_to_return = string_to_return + import_.abstract_syntax_tree() + "\n"
            string_to_return = string_to_return + "</IMPORT_LIST>\n"
        if len(self.variables_list) != 0:
            string_to_return = string_to_return + "<VARIABLE_LIST>\n"
            for variable in self.variables_list:
                string_to_return = string_to_return + variable.abstract_syntax_tree() + "\n"
            string_to_return = string_to_return + "</VARIABLE_LIST>\n"
        if self.constructor.function_name != "":
            string_to_return = string_to_return + "<CONSTRUCTOR_DECLARATION>\n"
            string_to_return = string_to_return + self.constructor.abstract_syntax_tree() + "\n"
            string_to_return = string_to_return + "</CONSTRUCTOR_DECLARATION>\n"
        if len(self.functions_list) != 0:
            string_to_return = string_to_return + "<FUNCTION_LIST>\n"
            for function in self.functions_list:
                string_to_return = string_to_return + function.abstract_syntax_tree() + "\n"
            string_to_return = string_to_return + "</FUNCTION_LIST>\n"
        if len(self.instructions_list) != 0:
            string_to_return = string_to_return + "<INSTRUCTION_LIST>\n"
            for instruction in self.instructions_list:
                if isinstance(instruction, str):
                    string_to_return = string_to_return + instruction + "\n"
                else:
                    string_to_return = string_to_return + instruction.abstract_syntax_tree() + "\n"
            string_to_return = string_to_return + "</INSTRUCTION_LIST>\n"
        string_to_return = string_to_return + "</CLASS>"
        return string_to_return
