from Objects.CallFunctionObject import CallFunctionObject
from Objects.ClassObject import ClassObject

# This class represent a class without "class" key instance
# A class is formed from:
# - a name
# - a list of imports
# - other classes with "class" key
# - a constructor with "__init__" key
# - some functions with "def" key
# - variables
# - instructions
class FileObject(ClassObject):
    class_list = list()

    def __init__(self):
        super().__init__()
        self.class_list = list()

    def add_class(self, class_object):
        self.class_list.append(class_object)

    def get_class_list(self):
        return self.class_list

    def abstract_syntax_tree(self, number_of_tabs):
        string_tabs = (number_of_tabs + 1) * "\t"
        string_to_return = "<FILE>(id," + self.class_name + ")\n"
        if len(self.import_list) != 0:
            string_to_return = string_to_return + string_tabs + "<IMPORT_LIST>\n"
            for import_ in self.import_list:
                string_to_return = string_to_return + import_.abstract_syntax_tree(number_of_tabs + 1) + "\n"
            string_to_return = string_to_return + string_tabs + "</IMPORT_LIST>\n"
        if len(self.variables_list) != 0:
            string_to_return = string_to_return + string_tabs + "<VARIABLE_LIST>\n"
            for variable in self.variables_list:
                string_to_return = string_to_return + variable.abstract_syntax_tree(number_of_tabs + 1) + "\n"
            string_to_return = string_to_return + string_tabs + "</VARIABLE_LIST>\n"
        if self.constructor.function_name != "":
            string_to_return = string_to_return + string_tabs + "<CONSTRUCTOR_DECLARATION>\n"
            string_to_return = string_to_return + self.constructor.abstract_syntax_tree(number_of_tabs + 1) + "\n"
            string_to_return = string_to_return + string_tabs + "</CONSTRUCTOR_DECLARATION>\n"
        if len(self.functions_list) != 0:
            string_to_return = string_to_return + string_tabs + "<FUNCTION_LIST>\n"
            for function in self.functions_list:
                string_to_return = string_to_return + function.abstract_syntax_tree(number_of_tabs + 1) + "\n"
            string_to_return = string_to_return + string_tabs + "</FUNCTION_LIST>\n"
        if len(self.class_list) != 0:
            string_to_return = string_to_return + string_tabs + "<CLASS_LIST>\n"
            for clas in self.class_list:
                string_to_return = string_to_return + clas.abstract_syntax_tree(number_of_tabs + 1) + "\n"
            string_to_return = string_to_return + string_tabs + "</CLASS_LIST>\n"
        if len(self.instructions_list) != 0:
            string_to_return = string_to_return + string_tabs + "<INSTRUCTION_LIST>\n"
            for instruction in self.instructions_list:
                if isinstance(instruction, CallFunctionObject):
                    string_to_return = string_to_return + instruction.abstract_syntax_tree(number_of_tabs) + "\n"
                else:
                    string_to_return = string_to_return + instruction.abstract_syntax_tree(number_of_tabs + 1) + "\n"
            string_to_return = string_to_return + string_tabs + "</INSTRUCTION_LIST>\n"
        if number_of_tabs == 1:
            string_to_return = string_to_return + "\t"
        string_to_return = string_to_return + "</FILE>\n"
        return string_to_return
