class MatrixContainer:
    class_name_list = []
    association_matrix = [[0] * 2 for _ in range(2)]
    invoked_method_in_inherited_method_matrix = [[0] * 2 for _ in range(2)]

    def __init__(self):
        self.class_name_list = []
        self.association_matrix = [[0] * 2 for _ in range(2)]
        self.invoked_method_in_inherited_method_matrix = [[0] * 2 for _ in range(2)]

    def set_class_name_list(self, class_name_list):
        self.class_name_list = class_name_list

    def get_class_name_list(self):
        return self.get_class_name_list()

    def get_association_matrix(self):
        return self.association_matrix

    def set_association_matrix(self, association_matrix):
        self.association_matrix = association_matrix

    def get_invoked_method_in_inherited_method_matrix(self):
        return self.invoked_method_in_inherited_method_matrix

    def set_invoked_method_in_inherited_method_matrix(self, invoked_method_in_inherited_method_matrix):
        self.invoked_method_in_inherited_method_matrix = invoked_method_in_inherited_method_matrix
