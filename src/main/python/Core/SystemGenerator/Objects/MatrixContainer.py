class MatrixContainer:
    # class_name_list = []
    class_name_list = ""
    # association_matrix = pd.DataFrame([[0, 0], [0, 0]])
    association_matrix = ""
    # generalization_matrix = pd.DataFrame([[0, 0], [0, 0]])
    generalization_matrix = ""
    # association_with_inheritance_matrix = pd.DataFrame([[0, 0], [0, 0]])
    association_with_inheritance_matrix = ""
    # association_with_inheritance_behavioral_data = BehavioralData()
    association_with_inheritance_behavioral_data = ""
    # invoked_method_in_inherited_method_matrix = pd.DataFrame([[0, 0], [0, 0]])
    invoked_method_in_inherited_method_matrix = ""
    invoked_method_in_inherited_method_behavioral_data = ""
    # Actually store this but i don't know if is usefully for me
    # double_dispatch_matrix = pd.DataFrame([[0, 0], [0, 0]])
    double_dispatch_matrix = ""
    # Actually store this but i don't know if is usefully for me
    # double_dispatch_behavioral_data = BehavioralData()
    double_dispatch_behavioral_data = ""
    # method_invocations_matrix = pd.DataFrame([[0, 0], [0, 0]])
    method_invocations_matrix = ""

    def __init__(self):
        self.class_name_list = ""
        self.association_matrix = ""
        self.generalization_matrix = ""
        self.association_with_inheritance_matrix = ""
        self.association_with_inheritance_behavioral_data = ""
        self.invoked_method_in_inherited_method_matrix = ""
        self.invoked_method_in_inherited_method_behavioral_data = ""
        self.double_dispatch_matrix = ""
        self.double_dispatch_behavioral_data = ""
        self.method_invocations_matrix = ""

    def set_class_name_list(self, class_name_list):
        self.class_name_list = class_name_list

    def get_class_name_list(self):
        return self.class_name_list

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

    def get_invoked_method_in_inherited_method_behavioral_data(self):
        return self.invoked_method_in_inherited_method_behavioral_data

    def set_invoked_method_in_inherited_method_behavioral_data(self, invoked_method_in_inherited_method_behavioral_data):
        self.invoked_method_in_inherited_method_behavioral_data = invoked_method_in_inherited_method_behavioral_data

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

    def __str__(self):
        string_to_return = ""
        if not isinstance(self.class_name_list, str):
            string_to_return = string_to_return + "\nClass Name List: " + str(self.class_name_list)
        if not isinstance(self.association_matrix, str):
            string_to_return = string_to_return + "\nAssociation Matrix: \n" + self.association_matrix.to_string()
        if not isinstance(self.generalization_matrix, str):
            string_to_return = string_to_return + "\nGeneralization Matrix: \n" + self.generalization_matrix.to_string()
        if not isinstance(self.invoked_method_in_inherited_method_matrix, str):
            string_to_return = string_to_return + "\nInvoked Method In Inherited Method Matrix: \n" \
                               + self.invoked_method_in_inherited_method_matrix.to_string()
        return string_to_return
