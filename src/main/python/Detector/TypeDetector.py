from Objects.CallFunctionObject import CallFunctionObject
from Objects.VariableObject import VariableObject
from Utils.ScopeGesture import Scope


class TypeDetector:
    variable_scope = {}

    def __init__(self, system_object):
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
                        if system_object.get_class_object_with_class_name(call_function.get_method_name()) is not None:
                            variable.set_type(call_function.get_method_name())
                            if key not in self.variable_scope:
                                scope = Scope()
                                scope.set_class_name(key)
                                self.variable_scope[key] = scope
                            self.variable_scope[key].add_variable(variable)

    def detect_type_of_variables_classes(self, system_object):
        for variable_scope in self.variable_scope.values():
            for variable in variable_scope.get_variables_list():
                possible_constructor_invocation = variable.get_argument()
                if isinstance(possible_constructor_invocation, CallFunctionObject):
                    class_object = system_object.get_class_object_with_class_name(
                        possible_constructor_invocation.get_method_name())
                    if class_object is not None:
                        for parameter in possible_constructor_invocation.get_parameters_list():
                            if isinstance(parameter, CallFunctionObject):
                                parameter_class_object = system_object.get_class_object_with_class_name(
                                    parameter.get_method_name())
                                if parameter_class_object is not None:
                                    parameter_type = parameter.get_method_name()
                                    for variable_of_target_class in class_object.get_variables_list():
                                        variable_of_target_class.set_type(parameter_type)
