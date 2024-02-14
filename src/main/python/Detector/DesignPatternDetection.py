from Descriptors.AdapterPattern import AdapterPatternDescriptor


class DesignPatternDetection:

    design_pattern = ""
    matrix_container = ""
    pattern_result = ""

    def __init__(self):
        self.design_pattern = ""
        self.matrix_container = ""
        self.pattern_result = ""

    def set_design_pattern(self):
        apd = AdapterPatternDescriptor()
        apd.matrix_container.set_class_name_list(["Adapter/ConcreteCommand", "Adaptee/Receiver"])

        assoc_matrix = [[0] * 2 for _ in range(2)]
        assoc_matrix[0][1] = 1
        apd.matrix_container.set_association_matrix(assoc_matrix)

        adapt_matrix = [[0] * 2 for _ in range(2)]
        adapt_matrix[0][1] = 1
        apd.matrix_container.set_invoked_method_in_inherited_method_matrix(adapt_matrix)

        # Adaptee and Adapter class
        apd.set_number_of_hierarchies(2)

        division_array = [2, 2]
        apd.set_divisor_array(division_array)
        apd.set_method_role_name("Request()/Execute()")
        apd.set_field_role_name("adaptee/receiver")

        self.design_pattern = apd

    def generate_results(self):
        results = ""

