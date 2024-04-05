from Core.SystemGenerator.Objects.MatrixContainer import MatrixContainer


class AdapterPatternDescriptor(MatrixContainer):
    number_of_hierarchies = 0
    divisor_array = []
    method_role_name = ""
    field_role_name = ""

    def __init__(self):
        super().__init__()
        self.number_of_hierarchies = 0
        self.divisor_array = []
        self.method_role_name = ""
        self.field_role_name = ""

    def set_number_of_hierarchies(self, number_of_hierarchies):
        self.number_of_hierarchies = number_of_hierarchies

    def set_divisor_array(self, divisor_array):
        self.divisor_array = divisor_array

    def set_method_role_name(self, method_role_name):
        self.method_role_name = method_role_name

    def set_field_role_name(self, field_role_name):
        self.field_role_name = field_role_name

    def get_divisor_with_position(self, position):
        if len(self.divisor_array) != 0:
            return self.divisor_array[position]
        return 0

    def get_divisor_with_role_name(self, role_name):
        pos = self.get_class_name_list().index(role_name)
        return self.get_divisor_with_position(pos)

    def get_number_of_hierarchies(self):
        return self.number_of_hierarchies

    def get_method_role_name(self):
        return self.method_role_name

    def get_field_role_name(self):
        return self.field_role_name
