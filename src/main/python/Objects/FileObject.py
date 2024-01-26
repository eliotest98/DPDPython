from Objects.FunctionObject import FunctionObject


# This class represent a class without "class" key instance
# A class is formed from:
# - a name
# - a list of imports
# - other classes with "class" key (optionals)
# - a constructor with "__init__" key (optionals)
# - some functions with "def" key (optionals)
# - variables (optionals)
# - instructions:
#   - call methods

class FileObject:
    class_name = ""
    class_list = list()
    functions_list = list()
    constructor = FunctionObject()
    variables_list = list()
    instructions = list()
    import_list = list()

    def __init__(self):
        self.class_name = ""
        self.class_list = list()
        self.functions_list = list()
        self.constructor = FunctionObject()
        self.variables_list = list()
        self.instructions = list()
        self.import_list = list()

    def set_class_name(self, class_name):
        self.class_name = class_name

    def add_class(self, class_object):
        self.class_list.append(class_object)

    def add_function(self, function_object):
        self.functions_list.append(function_object)

    def set_constructor(self, function_object):
        self.constructor = function_object

    def add_variable(self, variable_object):
        self.variables_list.append(variable_object)

    def add_instruction(self, call_function_object):
        self.instructions.append(call_function_object)

    def add_import(self, import_object):
        self.import_list.append(import_object)

    def to_string(self):
        string_to_return = "Main Class Name: " + self.class_name + "\n"
        if len(self.import_list) != 0:
            string_to_return = string_to_return + "Imports: \n"
            for import_ in self.import_list:
                string_to_return = string_to_return + import_.to_string() + "\n"
        if len(self.variables_list) != 0:
            string_to_return = string_to_return + "Variables: \n"
            for variable in self.variables_list:
                string_to_return = string_to_return + variable.to_string() + "\n"
        if self.constructor.function_name != "":
            string_to_return = string_to_return + "Constructor: \n" + self.constructor.to_string() + "\n"
        if len(self.functions_list) != 0:
            string_to_return = string_to_return + "Functions: \n"
            for function in self.functions_list:
                string_to_return = string_to_return + function.to_string() + "\n"
        if len(self.class_list) != 0:
            string_to_return = string_to_return + "Classes: \n"
            for clas in self.class_list:
                string_to_return = string_to_return + clas.to_string() + "\n"
        if len(self.instructions) != 0:
            string_to_return = string_to_return + "Instructions: \n"
            for instruction in self.instructions:
                if isinstance(instruction, str):
                    string_to_return = string_to_return + instruction + "\n"
                else:
                    string_to_return = string_to_return + instruction.to_string() + "\n"
        return string_to_return

    def abstract_syntax_tree(self):
        string_to_return = "<CLASS> (id," + self.class_name + ")\n"
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
        if len(self.class_list) != 0:
            string_to_return = string_to_return + "<CLASS_LIST>\n"
            for clas in self.class_list:
                string_to_return = string_to_return + clas.abstract_syntax_tree() + "\n"
            string_to_return = string_to_return + "</CLASS_LIST>\n"
        if len(self.instructions) != 0:
            string_to_return = string_to_return + "<INSTRUCTION_LIST>\n"
            for instruction in self.instructions:
                if isinstance(instruction, str):
                    string_to_return = string_to_return + instruction + "\n"
                else:
                    string_to_return = string_to_return + instruction.abstract_syntax_tree() + "\n"
            string_to_return = string_to_return + "</INSTRUCTION_LIST>\n"
        string_to_return = string_to_return + "</CLASS>"
        return string_to_return
