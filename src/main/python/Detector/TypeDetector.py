from Detector.ImportsDetector import ImportsDetector
from Objects.CallFunctionObject import CallFunctionObject
from Objects.FileObject import FileObject
from Objects.VariableObject import VariableObject
from Utils.ScopeGesture import Scope


class TypeDetector:
    variable_scope = {}
    imports_detector = ""

    def __init__(self, system_object):
        self.variable_scope = {}
        self.imports_detector = ""
        self.imports_detector = ImportsDetector(system_object)
        self.detect_type_with_call_functions(system_object)
        self.detect_type_of_variables_classes(system_object)

    def detect_type_with_call_functions(self, system_object):
        for i in range(system_object.get_class_number()):
            class_or_file_object = system_object.get_class_object_with_position(i)
            class_name = class_or_file_object.get_class_name()
            file_name = class_or_file_object.get_file_name()
            key = file_name + "." + class_name
            if file_name is None or file_name == "":
                key = class_name
            for variable in class_or_file_object.get_instructions_list():
                if isinstance(variable, VariableObject):
                    call_function = variable.get_argument()
                    if isinstance(call_function, CallFunctionObject):
                        origin_class = self.imports_detector.control_an_import(call_function.get_method_name())
                        if origin_class is None:
                            origin_class = key
                        if system_object.get_class_object_with_class_name(
                                origin_class + "." + call_function.get_method_name()) is not None:
                            variable.set_type(origin_class + "." + call_function.get_method_name())
                            if key not in self.variable_scope:
                                scope = Scope()
                                scope.set_class_name(key)
                                self.variable_scope[key] = scope
                            self.variable_scope[key].add_variable(variable)
                        elif isinstance(class_or_file_object, FileObject):
                            for single_class in class_or_file_object.get_class_list():
                                if single_class.get_class_name() == call_function.get_method_name():
                                    variable.set_type(origin_class + "." + call_function.get_method_name())
                                    if key not in self.variable_scope:
                                        scope = Scope()
                                        scope.set_class_name(key)
                                        self.variable_scope[key] = scope
                                    self.variable_scope[key].add_variable(variable)

    def detect_type_of_variables_classes(self, system_object):
        for file_name in self.variable_scope:
            variable_scope = self.variable_scope[file_name]
            for variable in variable_scope.get_variables_list():
                possible_constructor_invocation = variable.get_argument()
                if isinstance(possible_constructor_invocation, CallFunctionObject):
                    class_object = system_object.get_class_object_with_class_name(variable.get_type())
                    if class_object is not None:
                        for parameter in possible_constructor_invocation.get_parameters_list():
                            if isinstance(parameter, CallFunctionObject):
                                origin_class = self.imports_detector.control_an_import(parameter.get_method_name())
                                if origin_class is None:
                                    origin_class = file_name
                                target_class = origin_class + "." + parameter.get_method_name()
                                parameter_class_object = system_object.get_class_object_with_class_name(target_class)
                                if parameter_class_object is not None:
                                    for variable_of_target_class in class_object.get_variables_list():
                                        variable_of_target_class.set_type(target_class)
