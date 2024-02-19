# This class detect the superclasses of a specific class
from Objects.CallFunctionObject import CallFunctionObject
from Objects.FileObject import FileObject
from Objects.VariableObject import VariableObject


class SuperclassDetector:
    functions_list_of_classes = {}

    def __init__(self, system_object):
        self.get_all_functions(system_object)
        self.detect_with_functions(system_object)

    def get_all_functions(self, system_object):
        for i in range(system_object.get_class_number()):
            class_object = system_object.get_class_object_with_position(i)
            if isinstance(class_object, FileObject):
                for single_class in class_object.get_class_list():
                    key = single_class.get_file_name() + "." + single_class.get_class_name()
                    for function_object in single_class.get_functions_list():
                        if key not in self.functions_list_of_classes:
                            self.functions_list_of_classes[key] = list()
                        self.functions_list_of_classes[key].append(function_object.get_function_name())

    def detect_with_functions(self, system_object):
        for i in range(system_object.get_class_number()):
            class_object = system_object.get_class_object_with_position(i)
            if isinstance(class_object, FileObject):
                for single_class in class_object.get_class_list():
                    for function_object in single_class.get_functions_list():
                        # This is for the instruction list
                        method_name = self.recursive_detection(function_object.get_instructions_list())
                        if method_name is not None:
                            method_name = method_name.removeprefix(".")
                            for class_name, methods_list in self.functions_list_of_classes.items():
                                for inside_method in methods_list:
                                    if inside_method == method_name:
                                        split = class_name.split(".")
                                        single_class.add_superclass(split[len(split) - 1])
                        # This is for the return
                        if isinstance(function_object.get_return_object().get_argument(), CallFunctionObject):
                            method_name = function_object.get_return_object().get_argument().get_method_name()
                            if method_name is not None:
                                method_name = method_name.removeprefix(".")
                                for class_name, methods_list in self.functions_list_of_classes.items():
                                    for inside_method in methods_list:
                                        if inside_method == method_name:
                                            split = class_name.split(".")
                                            single_class.add_superclass(split[len(split) - 1])

    def recursive_detection(self, list_):
        if isinstance(list_, CallFunctionObject):
            return list_.get_method_name()
        elif isinstance(list_, VariableObject):
            self.recursive_detection(list_.get_argument())
        else:
            for instruction in list_:
                self.recursive_detection(instruction)
