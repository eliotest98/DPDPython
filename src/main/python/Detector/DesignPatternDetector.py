from Core.SystemGenerator.Objects.ClusterResult import ClusterResult
from Descriptors.AdapterPattern import AdapterPatternDescriptor
import numpy as np

from Utils import MatrixGesture


class SimilarityAlgorithm:
    TOLERANCE = 0.001  # Define your tolerance value here

    # TODO da inserire tutte le matrici
    def get_total_score(self, system_container, pattern_descriptor):
        x = np.zeros((len(pattern_descriptor.get_class_name_list()), len(system_container.get_class_name_list())))
        if pattern_descriptor.get_double_dispatch_matrix() is not None:
            if self.all_elements_equal_to_zero(system_container.get_double_dispatch_matrix()):
                return None
            else:
                x = np.add(x, self.get_similarity_score(system_container.get_double_dispatch_matrix(),
                                                        pattern_descriptor.get_double_dispatch_matrix()))
        for i in range(len(x)):
            for j in range(len(x[i])):
                x[i][j] = x[i][j] / float(pattern_descriptor.get_divisor(i))
        return x

    def all_elements_equal_to_zero(self, m):
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] != 0.0:
                    return False
        return True

    def norm1(self, m):
        f = 0
        for j in range(len(m[0])):
            s = 0
            for i in range(len(m)):
                s += abs(m[i][j])
            f = max(f, s)
        return f

    def get_similarity_score(self, a, b):
        m = len(a)  # row dimension
        n = len(b[0])  # column dimension

        if np.array_equal(a, np.zeros((len(a), len(a[0])))) or np.array_equal(b, np.zeros((len(b), len(b[0])))):
            return np.zeros((n, m))

        x = MatrixGesture.fill(n, m, 1.0)
        prev_x = np.zeros((n, m))
        flag = False
        i = 0

        while not flag:
            temp1 = MatrixGesture.times(MatrixGesture.times(b, x), MatrixGesture.transpose(a))
            temp2 = MatrixGesture.times(MatrixGesture.times(MatrixGesture.transpose(b), x), a)
            temp = MatrixGesture.plus(temp1, temp2)
            x = MatrixGesture.divide(temp, self.norm1(temp))
            i += 1

            if i % 2 == 0:
                flag = self.convergence(x, prev_x)
                prev_x = x

        return x

    def convergence(self, a, b):
        for i in range(len(a)):
            for j in range(len(a[i])):
                if abs(a[i][j] - b[i][j]) > self.TOLERANCE:
                    return False
        return True


class DesignPatternDetection:
    design_pattern = ""
    matrix_container = ""
    pattern_result = ""

    def __init__(self):
        self.design_pattern = ""
        self.matrix_container = ""
        self.pattern_result = ""

    # This method set the base of AdapterPattern
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

    def generate_results(self, system_container, pattern_descriptor, pattern_result):
        results = SimilarityAlgorithm.get_total_score(system_container, pattern_descriptor)
        if results is not None:
            cluster_result = ClusterResult(results, pattern_descriptor, system_container)
            list = cluster_result.get_pattern_instance_list()
            for pi in list:
                if not pattern_result.contains_instance(pi):
                    pattern_result.add_instance(pi)
