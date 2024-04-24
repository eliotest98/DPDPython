class Scope:
    class_name = ""
    variable_list = list()

    def __init__(self):
        self.class_name = ""
        self.variable_list = list()

    def set_class_name(self, class_name):
        self.class_name = class_name

    def get_class_name(self):
        return self.class_name

    def add_variable(self, variable_object):
        self.variable_list.append(variable_object)

    def get_variables_list(self):
        return self.variable_list

    def __contains__(self, item):
        for variable in self.variable_list:
            variable_name = item.get_variable_name()
            if str(variable_name).__contains__("."):
                variable_name = str(variable_name).removeprefix("self.")
            if variable.get_variable_name() == variable_name:
                return True
        return False
