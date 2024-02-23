from Utils.ScopeGesture import Scope


class ScopeDetector:
    variable_scope = {}

    def __init__(self, system_object):
        self.get_all_variables(system_object)
        self.detect_scope(system_object)

    def get_variables_scope(self):
        return self.variable_scope

    def get_all_variables(self, system_object):
        for i in range(system_object.get_class_number()):
            class_or_file_object = system_object.get_class_object_with_position(i)
            class_name = class_or_file_object.get_class_name()
            file_name = class_or_file_object.get_file_name()
            key = file_name + "." + class_name
            if file_name is None or file_name == "":
                key = class_name
            for variable in class_or_file_object.get_variables_list():
                if key not in self.variable_scope:
                    scope = Scope()
                    scope.set_class_name(key)
                    self.variable_scope[key] = scope
                self.variable_scope[key].add_variable(variable)

    def detect_scope(self, system_object):
        for scope in self.variable_scope.values():
            if scope.get_class_name().__contains__("."):
                if scope.get_class_name().split(".")[0] in self.variable_scope:
                    father = self.variable_scope[scope.get_class_name().split(".")[0]]
                    for variable in scope.get_variables_list():
                        if father.__contains__(variable):
                            self.change_variable_to_instruction(variable, scope.get_class_name(), system_object)

    def change_variable_to_instruction(self, variable_to_change, class_to_change, system_object):
        for i in range(system_object.get_class_number()):
            class_or_file_object = system_object.get_class_object_with_position(i)
            class_name = class_or_file_object.get_class_name()
            file_name = class_or_file_object.get_file_name()
            key = file_name + "." + class_name
            if file_name is None or file_name == "":
                key = class_name
            if key == class_to_change:
                class_or_file_object.remove_variable(variable_to_change)
                class_or_file_object.add_instruction(variable_to_change)
