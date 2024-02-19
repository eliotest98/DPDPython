from Core.SystemGenerator.Objects.BehavioralData import BehavioralData


class MatrixContainer:
    class_name_list = []
    association_matrix = [[0] * 2 for _ in range(2)]
    generalization_matrix = [[0] * 2 for _ in range(2)]
    association_with_inheritance_matrix = [[0] * 2 for _ in range(2)]
    association_with_inheritance_behavioral_data = BehavioralData()
    invoked_method_in_inherited_method_matrix = [[0] * 2 for _ in range(2)]
    # Actually store this but i don't know if is usefully for me
    double_dispatch_matrix = [[0] * 2 for _ in range(2)]
    # Actually store this but i don't know if is usefully for me
    double_dispatch_behavioral_data = BehavioralData()
    method_invocations_matrix = [[0] * 2 for _ in range(2)]

    def __init__(self):
        self.class_name_list = []
        self.association_matrix = [[0] * 2 for _ in range(2)]
        self.generalization_matrix = [[0] * 2 for _ in range(2)]
        self.association_with_inheritance_matrix = [[0] * 2 for _ in range(2)]
        self.association_with_inheritance_behavioral_data = BehavioralData()
        self.invoked_method_in_inherited_method_matrix = [[0] * 2 for _ in range(2)]
        self.double_dispatch_matrix = [[0] * 2 for _ in range(2)]
        self.double_dispatch_behavioral_data = BehavioralData()

    def set_class_name_list(self, class_name_list):
        self.class_name_list = class_name_list

    def get_class_name_list(self):
        return self.get_class_name_list()

    def get_association_matrix(self):
        return self.association_matrix

    def set_association_matrix(self, association_matrix):
        self.association_matrix = association_matrix

    def get_generalization_matrix(self):
        return self.generalization_matrix

    def set_generalization_matrix(self, generalization_matrix):
        self.generalization_matrix = generalization_matrix

    def get_invoked_method_in_inherited_method_matrix(self):
        return self.invoked_method_in_inherited_method_matrix

    def set_invoked_method_in_inherited_method_matrix(self, invoked_method_in_inherited_method_matrix):
        self.invoked_method_in_inherited_method_matrix = invoked_method_in_inherited_method_matrix

    def set_association_with_inheritance_matrix(self, association_with_inheritance_matrix):
        self.association_with_inheritance_matrix = association_with_inheritance_matrix

    def get_association_with_inheritance_matrix(self):
        return self.association_with_inheritance_matrix

    def set_association_with_inheritance_behavioral_data(self, association_with_inheritance_behavioral_data):
        self.association_with_inheritance_behavioral_data = association_with_inheritance_behavioral_data

    def get_association_with_inheritance_behavioral_data(self):
        return self.association_with_inheritance_behavioral_data

    def get_double_dispatch_matrix(self):
        return self.double_dispatch_matrix

    def set_double_dispatch_matrix(self, double_dispatch_matrix):
        self.double_dispatch_matrix = double_dispatch_matrix

    def get_double_dispatch_behavioral_data(self):
        return self.double_dispatch_behavioral_data

    def set_double_dispatch_behavioral_data(self, double_dispatch_behavioral_data):
        self.double_dispatch_behavioral_data = double_dispatch_behavioral_data

    def get_method_invocations_matrix(self):
        return self.method_invocations_matrix

    def set_method_invocations_matrix(self, method_invocations_matrix):
        self.method_invocations_matrix = method_invocations_matrix

