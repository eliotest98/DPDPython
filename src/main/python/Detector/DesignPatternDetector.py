import pandas
import pandas as pd
from pandas import DataFrame

from Core.SystemGenerator.Objects.ClusterResult import ClusterResult
from Descriptors.AdapterPattern import AdapterPatternDescriptor
import numpy as np
from Utils import MatrixGesture


class SimilarityAlgorithm:
    TOLERANCE = 0.001  # Define your tolerance value here

    # TODO da inserire tutte le matrici
    def get_total_score(self, system_container, pattern_descriptor):
        x = [[0 for _ in range(len(system_container.get_class_name_list()))] for _ in
             range(len(pattern_descriptor.get_class_name_list()))]

        # if pattern_descriptor.get_double_dispatch_matrix() is not None:
        #    if self.all_elements_equal_to_zero(system_container.get_double_dispatch_matrix()):
        #        return None
        #    else:
        #        x = np.add(x, self.get_similarity_score(system_container.get_double_dispatch_matrix(),
        #                                                pattern_descriptor.get_double_dispatch_matrix()))
        if pattern_descriptor.get_association_matrix() is not None:
            if self.all_elements_equal_to_zero(system_container.get_association_matrix()):
                return None
            else:
                association_starts_from_role = -1
                association_ends_to_role = -1
                p = pattern_descriptor.get_association_matrix()
                for i in range(len(p.columns)):
                    for j in range(len(p.index)):
                        if p[p.columns[i]][p.index[j]] == 1.0:
                            association_starts_from_role = i
                            association_ends_to_role = j

                temp = self.get_similarity_score(system_container.get_association_matrix(),
                                                 pattern_descriptor.get_association_matrix())

                role_maps = {0: {}, 1: {}}
                for i in range(len(temp)):
                    for j in range(len(temp.columns)):
                        value = temp.iloc[i, j]
                        if 0 < value < 0.01:
                            # Ottieni il dizionario corrispondente all'indice di riga
                            role_map = role_maps.get(i)

                            # Formatta il valore come stringa
                            score = "{:.15f}".format(value)

                            # Se la chiave non esiste nel dizionario, crea una nuova lista
                            if score not in role_map:
                                role_map[score] = [j]
                            # Altrimenti, aggiungi l'indice alla lista esistente
                            else:
                                role_map[score].append(j)

                association_starts_from_role_map = role_maps.get(association_starts_from_role)
                association_ends_to_role_map = role_maps.get(association_ends_to_role)
                for score in association_starts_from_role_map.keys():
                    association_starts_from_classes = association_starts_from_role_map.get(score)
                    association_ends_to_classes = association_ends_to_role_map.get(score)
                    system_association_matrix = system_container.getAssociationMatrix()
                    if association_starts_from_classes is not None and association_ends_to_classes is not None:
                        for i in association_starts_from_classes:
                            for j in association_ends_to_classes:
                                if system_association_matrix[i][j] == 1.0:
                                    if temp[association_starts_from_role][i] != 1.0:
                                        temp[association_starts_from_role][i] = 1.0
                                    if temp[association_ends_to_role][j] != 1.0:
                                        temp[association_ends_to_role][j] = 1.0
                x = MatrixGesture.plus(pd.DataFrame(x, index=temp.index, columns=temp.columns), temp)

        for i in range(len(x)):
            divisor = pattern_descriptor.get_divisor_with_position(i)
            x.iloc[i] = x.iloc[i] / divisor

        return x

    def get_similarity_score(self, a, b):
        m, n = a.shape[0], b.shape[1]
        if (a.values == np.zeros((m, a.shape[1]))).all() or (b.values == np.zeros((b.shape[0], n))).all():
            return pd.DataFrame(np.zeros((n, m)))

        x = MatrixGesture.fill(n, m, 1.0, a.index)
        prev_x = pd.DataFrame(np.zeros((n, m)), index=a.index, columns=a.index)
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

    def all_elements_equal_to_zero(self, m):
        return m.nunique().sum() <= 1

    def norm1(self, m):
        # Calculates the absolute sum of each column
        s = m.abs().sum(axis=0)

        # Find the maximum of the sums
        f = s.max()

        return f

    def convergence(self, a, b):
        # Calcola la differenza assoluta tra le due matrici
        diff = np.abs(a - b)

        # Controlla se ogni elemento della differenza è inferiore alla tolleranza
        if (diff > self.TOLERANCE).any().any():
            return False
        else:
            return True


class DesignPatternDetection:
    similarity_algorithm = SimilarityAlgorithm()

    def __init__(self):
        self.similarity_algorithm = SimilarityAlgorithm()

    # This method set the base of a design pattern, actually there is only Adapter Pattern
    def set_design_pattern(self, design_pattern_name):
        apd = AdapterPatternDescriptor()
        apd.set_class_name_list(["Adapter/ConcreteCommand", "Adaptee/Receiver"])

        assoc_matrix = [[0, 0], [0, 0]]
        assoc_matrix[0][1] = 1
        labels = ['Adaptee', 'Adapter']
        df_assoc_matrix = pd.DataFrame(assoc_matrix, index=labels, columns=labels)
        apd.set_association_matrix(df_assoc_matrix)

        adapt_matrix = [[0, 0], [0, 0]]
        adapt_matrix[0][1] = 1
        labels = ['Pippo', 'Pluto']
        df_adapt_matrix = pd.DataFrame(adapt_matrix, index=labels, columns=labels)
        apd.set_invoked_method_in_inherited_method_matrix(df_adapt_matrix)

        # Adaptee and Adapter class
        apd.set_number_of_hierarchies(2)

        # TODO chiedere al prof cosa può essere (in origine è division_array = [2,2])
        division_array = [1, 1]
        apd.set_divisor_array(division_array)
        apd.set_method_role_name("Request()/Execute()")
        apd.set_field_role_name("adaptee/receiver")

        return apd

    def generate_results(self, system_container, pattern_descriptor, pattern_result):
        results = self.similarity_algorithm.get_total_score(system_container, pattern_descriptor)
        if results is not None:
            cluster_result = ClusterResult(results, pattern_descriptor, system_container)
            list = cluster_result.get_pattern_instance_list()
            for pi in list:
                if not pattern_result.contains_instance(pi):
                    pattern_result.add_instance(pi)
