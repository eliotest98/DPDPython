import numpy as np
import pandas as pd

from Core.SystemGenerator.Hierarchy.HierarchyDetection import HierarchyDetection
from Core.SystemGenerator.Hierarchy.InheritanceHierarchy import InheritanceHierarchy
from Core.SystemGenerator.Objects.BehavioralData import BehavioralData
from Core.SystemGenerator.Objects.ClusterSet import ClusterSet, Entry
from Core.SystemGenerator.Objects.MatrixContainer import MatrixContainer
from Objects.CallFunctionObject import CallFunctionObject
from Objects.VariableObject import VariableObject


class SystemGenerator:
    system_object = ""
    matrix_container = ""
    hierarchy_list = list()

    def __init__(self, system_object):
        self.system_object = system_object
        self.matrix_container = MatrixContainer()
        self.hierarchy_list = HierarchyDetection(system_object).get_hierarchy_list()

        self.matrix_container.set_class_name_list(self.system_object.get_class_names())
        self.matrix_container.set_generalization_matrix(self.get_generalization_matrix())
        self.matrix_container.set_association_matrix(self.get_association_matrix())
        self.association_with_inheritance_matrix()
        self.double_dispatch_matrix()
        self.matrix_container.set_method_invocations_matrix(self.get_method_invocations_matrix())

    def get_method_invocations_matrix(self):
        m = pd.DataFrame(np.zeros((self.system_object.get_class_number(), self.system_object.get_class_number())))

        counter = 0
        index = list()

        for co in self.system_object.get_class_list_iterator():
            index.append(co.get_class_name())
            discrete_invocations = []
            # Iterate on each FunctionObject in the class
            for mo in co.get_functions_list():
                # Iterate on each instruction of function
                for mio in mo.get_instructions_list():
                    # Control if is a VariableObject with CallFunctionMethod
                    if isinstance(mio, VariableObject):
                        if isinstance(mio.get_argument(), CallFunctionObject):
                            if mio not in discrete_invocations:
                                discrete_invocations.append(mio)
                                pos = self.system_object.get_position_in_class_list(
                                    mio.get_argument().get_original_class_name())
                                if pos != -1 and counter != pos:
                                    m.iloc[counter, pos] += 1.0
                                    m.iloc[pos, counter] += 1.0
                    elif isinstance(mio, CallFunctionObject):
                        if mio not in discrete_invocations:
                            discrete_invocations.append(mio)
                            pos = self.system_object.get_position_in_class_list(
                                mio.get_original_class_name())
                            if pos != -1 and counter != pos:
                                m.iloc[counter, pos] += 1.0
                                m.iloc[pos, counter] += 1.0
                if isinstance(mo.get_return_object().get_argument(), CallFunctionObject):
                    if mo not in discrete_invocations:
                        discrete_invocations.append(mo)
                        pos = self.system_object.get_position_in_class_list(
                            mo.get_return_object().get_argument().get_original_class_name())
                        if pos != -1 and counter != pos:
                            m.iloc[counter, pos] += 1.0
                            m.iloc[pos, counter] += 1.0
            counter += 1
        m.index = index
        m.columns = index
        return m

    def get_generalization_matrix(self):
        m = [[0 for _ in range(self.system_object.get_class_number())] for _ in
             range(self.system_object.get_class_number())]
        counter = 0

        labels = list()

        for co in self.system_object.get_class_list_iterator():
            labels.append(co.get_class_name())
            for superclass in co.get_superclass_list():
                pos = self.system_object.get_position_in_class_list(superclass)
                if pos != -1:
                    m[counter][pos] = 1
            counter += 1

        return pd.DataFrame(m, index=labels, columns=labels)

    # This method create an association matrix with all classes of system
    # The target is seen the associations between classes with types of variables
    def get_association_matrix(self):
        assoc_matrix = [[0 for _ in range(self.system_object.get_class_number())] for _ in
                        range(self.system_object.get_class_number())]
        counter = 0
        labels = list()

        for co in self.system_object.get_class_list_iterator():
            labels.append(co.get_class_name())
            for fo in co.get_variables_list():
                if isinstance(fo, VariableObject):
                    class_type = fo.get_type()
                    if "[]" in class_type:
                        # Type[] is an array of associations
                        class_type = class_type[:-2]
                    pos = self.system_object.get_position_in_class_list(class_type)
                    if pos != -1 and counter != pos:
                        assoc_matrix[counter][pos] = 1

            counter += 1
        return pd.DataFrame(assoc_matrix, index=labels, columns=labels)

    def child_parent_relationship(self, child_class, parent_class):
        for ih in self.hierarchy_list:
            if isinstance(ih, InheritanceHierarchy):
                child_node = ih.get_node(child_class)
                parent_node = ih.get_node(parent_class)
                if child_node is not None and parent_node is not None:
                    current_parent = child_node.get('parent')
                    while current_parent is not None:
                        if current_parent.get('userObject') == parent_node.get('userObject'):
                            return True
                        current_parent = current_parent.get('parent')
        return False

    def association_with_inheritance_matrix(self):
        m = [[0 for _ in range(self.system_object.get_class_number())] for _ in
             range(self.system_object.get_class_number())]
        behavioral_data = BehavioralData()
        counter = 0
        labels = list()
        for co in self.system_object.get_class_list_iterator():
            labels.append(co.get_class_name())
            for fo in co.get_variables_list():
                class_type = fo.get_type()
                pos = self.system_object.get_position_in_class_list(class_type)
                if pos != -1 and counter != pos and self.child_parent_relationship(co.get_class_name(), class_type):
                    m[counter][pos] = 1
                    behavioral_data.add_field(counter, pos, fo)

            counter += 1

        self.matrix_container.set_association_with_inheritance_matrix(pd.DataFrame(m, index=labels, columns=labels))
        self.matrix_container.set_association_with_inheritance_behavioral_data(behavioral_data)

    def double_dispatch_matrix(self):
        m = [[0 for _ in range(self.system_object.get_class_number())] for _ in
             range(self.system_object.get_class_number())]
        behavioral_data = BehavioralData()
        counter = 0
        labels = list()

        for co in self.system_object.get_class_list_iterator():
            labels.append(co.get_class_name())
            # for mo in co.get_functions_list():

            # It's not possible have this information
            # for p in mo.get_parameter_list_iterator():
            #    parameter_type = p.get_class_type()
            #    pos = self.system_object.get_position_in_class_list(parameter_type)
            #    if pos != -1:

            #        for mio in mo.get_method_invocation_iterator():
            #            if mio.get_origin_class_name() == parameter_type and mio.has_parameter_type(co):
            #                temp = self.system_object.get_class_object(pos).get_method(mio.get_signature())
            #                if temp is not None and temp.is_abstract() and temp.get_name().startswith("visit"):
            #                    m[pos][counter] = 1
            #                    behavioral_data.add_method(pos, counter, mo)

            counter += 1

        self.matrix_container.set_double_dispatch_matrix(pd.DataFrame(m, index=labels, columns=labels))
        self.matrix_container.set_double_dispatch_behavioral_data(behavioral_data)

    def get_hierarchy_list(self):
        return self.hierarchy_list

    def generate_cluster_set(self, pattern_descriptor):
        cluster_set = ClusterSet()
        system_adjacency_matrix = self.matrix_container.get_method_invocations_matrix()

        for i in range(len(self.hierarchy_list)):
            ih1 = self.hierarchy_list[i]
            ih2 = None
            for j in range(i, len(self.hierarchy_list)):
                sum = 0
                ih1_nodes_checked = []
                all_relations = False
                for e1 in ih1.get_enumeration():
                    if isinstance(e1, str):
                        class_name1 = e1
                    else:
                        class_name1 = e1["userObject"]
                    if class_name1 not in ih1_nodes_checked:
                        ih1_nodes_checked.append(class_name1)
                        ih2 = self.hierarchy_list[j]
                        ih2_nodes_checked = []
                        for e2 in ih2.get_enumeration():
                            if isinstance(e2, str):
                                class_name2 = e2
                            else:
                                class_name2 = e2["userObject"]
                            if class_name2 not in ih2_nodes_checked:
                                ih2_nodes_checked.append(class_name2)
                                if class_name1 != class_name2:
                                    sum += system_adjacency_matrix[class_name1][class_name2]
                                    if self.cluster_with_all_relations(class_name1, class_name2, pattern_descriptor):
                                        all_relations = True

                if all_relations:
                    entry = Entry()
                    entry.add_hierarchy(ih1)
                    entry.add_hierarchy(ih2)
                    entry.set_number_of_method_invocations(int(sum))
                    cluster_set.add_cluster_entry(entry)

        return cluster_set

    # TODO qui bisogna aggiungere tutte le matrici
    def cluster_with_all_relations(self, class_name1, class_name2, pattern):
        total_relations = 0
        actual_relations = 0
        if pattern.matrix_container.get_association_matrix() is not None:
            total_relations = total_relations + 1
            if (self.matrix_container.get_association_matrix()[class_name1][class_name2] == 1 or
                    self.matrix_container.get_association_matrix()[class_name2][class_name1] == 1):
                actual_relations = actual_relations + 1
        # Repeat the above if block for each pattern matrix
        # ...
        return total_relations == actual_relations

    # TODO qui bisogna aggiungere tutte le matrici
    def get_hierarchies_matrix_container(self, hierarchy_list):
        hierarchies_class_name_list = []
        hierarchies_matrix_container = MatrixContainer()

        for ih in hierarchy_list:
            for e in ih.get_enumeration():
                if isinstance(e, str):
                    s = e
                else:
                    s = e["userObject"]
                if s not in hierarchies_class_name_list:
                    hierarchies_class_name_list.append(s)

        hierarchies_matrix_container.set_class_name_list(hierarchies_class_name_list)
        generalization_output = self.generate_hierarchies_matrix(hierarchies_class_name_list,
                                                                 self.matrix_container.get_generalization_matrix(),
                                                                 None)
        hierarchies_matrix_container.set_generalization_matrix(generalization_output[0])

        association_output = self.generate_hierarchies_matrix(hierarchies_class_name_list,
                                                              self.matrix_container.get_association_matrix(), None)

        hierarchies_matrix_container.set_association_matrix(association_output[0])

        # Repeat the above two lines for each pattern matrix
        # ...
        return hierarchies_matrix_container

    def generate_hierarchies_matrix(self, hierarchies_class_name_list, system_matrix, system_behavioral_data):
        hierarchies_matrix = pd.DataFrame([[0 for _ in range(len(hierarchies_class_name_list))] for _ in
                                           range(len(hierarchies_class_name_list))])
        hierarchies_behavioral_data = BehavioralData()

        for i in range(len(hierarchies_class_name_list)):
            class_name1 = hierarchies_class_name_list[i]
            hierarchies_matrix = hierarchies_matrix.rename(columns={i: class_name1})
            system_i = self.system_object.get_position_in_class_list(class_name1)
            for j in range(len(hierarchies_class_name_list)):
                class_name2 = hierarchies_class_name_list[j]
                hierarchies_matrix = hierarchies_matrix.rename(index={j: class_name2})
                system_j = self.system_object.get_position_in_class_list(class_name2)
                hierarchies_matrix[class_name1][class_name2] = system_matrix[class_name1][class_name2]
                if system_behavioral_data is not None:
                    fields = system_behavioral_data.get_fields(system_i, system_j)
                    if fields is not None:
                        hierarchies_behavioral_data.add_fields(i, j, fields)
                    methods = system_behavioral_data.get_methods(system_i, system_j)
                    if methods is not None:
                        hierarchies_behavioral_data.add_methods(i, j, methods)

        return hierarchies_matrix, hierarchies_behavioral_data
