from Detector.ScopeDetector import ScopeDetector
from Downloader.ProgressionCheck import ProgressDetection
from Objects.ClassObject import ClassObject
from Objects.VariableObject import VariableObject


class VariableDetector:
    progressor = ProgressDetection()

    def __init__(self, system_object, terminal):
        self.progressor = ProgressDetection()
        scope_detector = ScopeDetector(system_object, terminal)
        variables = scope_detector.get_variables_scope()
        self.detect_self_variables(system_object, variables, terminal)
        self.detect_same_variable_in_variables_list(system_object, terminal)

    def detect_self_variables(self, system_object, variables_in_scope, terminal):
        for i in range(system_object.get_class_number()):
            self.progressor.update(len(system_object.get_class_names()), i, "VariableDetector detect self variables",
                                   terminal)
            class_or_file_object = system_object.get_class_object_with_position(i)
            if isinstance(class_or_file_object, ClassObject):
                for function in class_or_file_object.get_functions_list():
                    self.control_and_creation_of_a_variable(function.get_variables_list(), variables_in_scope,
                                                            class_or_file_object)
                    self.control_and_creation_of_a_variable(function.get_instructions_list(), variables_in_scope,
                                                            class_or_file_object)

    def control_and_creation_of_a_variable(self, list_to_control, variables_in_scope, class_or_file_object):
        is_breaked = False
        for variable in list_to_control:
            if isinstance(variable, VariableObject):
                for scope in variables_in_scope.values():
                    if scope.__contains__(variable):
                        is_breaked = True
                        break
                if not is_breaked:
                    if str(variable.get_variable_name()).__contains__("self."):
                        new_variable = VariableObject()
                        new_variable.set_variable_name(variable.get_variable_name().removeprefix("self."))
                        new_variable.set_type(variable.get_type())
                        class_or_file_object.add_variable(new_variable)

    def detect_same_variable_in_variables_list(self, system_object, terminal):
        for i in range(system_object.get_class_number()):
            self.progressor.update(len(system_object.get_class_names()), i,
                                   "VariableDetector detect same variable in variable list", terminal)
            class_or_file_object = system_object.get_class_object_with_position(i)
            variables = list()
            for variable in class_or_file_object.get_variables_list():
                if len(variables) == 0:
                    variables.append(variable.get_variable_name())
                elif variables.__contains__(variable.get_variable_name()):
                    class_or_file_object.remove_variable(variable)
                    class_or_file_object.add_instruction(variable)
            for function in class_or_file_object.get_functions_list():
                variables = list()
                for variable in function.get_variables_list():
                    if len(variables) == 0:
                        variables.append(variable.get_variable_name())
                    elif variables.__contains__(variable.get_variable_name()):
                        function.remove_variable(variable)
                        function.add_instruction(variable)
