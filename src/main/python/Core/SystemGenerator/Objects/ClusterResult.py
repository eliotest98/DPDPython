from Core.SystemGenerator.Objects.MatrixContainer import MatrixContainer
from Core.SystemGenerator.Objects.PatternInstance import PatternInstance, RoleType
from Descriptors.AdapterPattern import AdapterPatternDescriptor
from Core.SystemGenerator.Objects.PatternInstance import Entry as piEntry
import re


class ClusterResult:
    entry_set = set()
    # TODO to change when implements others Descriptors
    pattern_descriptor = AdapterPatternDescriptor()
    system_container = MatrixContainer()

    def __init__(self, results, pattern_descriptor, system_container):
        self.entry_set = set()
        self.pattern_descriptor = pattern_descriptor
        self.system_container = system_container

        row_name_list = pattern_descriptor.get_class_name_list()
        column_name_list = system_container.get_class_name_list()
        for i in range(len(results)):
            for j in range(len(results.columns)):
                value = results.iloc[i, j]
                row_name = row_name_list[i]
                column_name = column_name_list[j]
                entry = Entry(value, row_name, column_name, j)
                self.entry_set.add(entry)

    def get_pattern_instance_list(self):
        role_map = {}

        for entry in self.entry_set:
            divisor = self.pattern_descriptor.get_divisor_with_role_name(entry.get_role())
            threshold = (divisor - 1) / divisor
            if entry.get_score() > threshold:
                if entry.get_role() in role_map:
                    entry_set = role_map[entry.get_role()]
                    entry_set.add(entry)
                else:
                    entry_set = set()
                    entry_set.add(entry)
                    role_map[entry.get_role()] = entry_set

        roles = list(role_map.keys())
        entry_tuple_set = set()
        if len(roles) > 0:
            for first_role_entry in role_map[roles[0]]:
                if len(roles) > 1:
                    for second_role_entry in role_map[roles[1]]:
                        if len(roles) == 2:
                            tuple = EntryTuple()
                            relationship_score = self.relationship_score(first_role_entry, second_role_entry)
                            tuple.add_pair(relationship_score, first_role_entry, second_role_entry)
                            entry_tuple_set.add(tuple)
                        elif len(roles) > 2:
                            for third_role_entry in role_map[roles[2]]:
                                tuple = EntryTuple()
                                first_second_relationship_score = self.relationship_score(first_role_entry,
                                                                                          second_role_entry)
                                tuple.add_pair(first_second_relationship_score, first_role_entry, second_role_entry)
                                first_third_relationship_score = self.relationship_score(first_role_entry,
                                                                                         third_role_entry)
                                tuple.add_pair(first_third_relationship_score, first_role_entry, third_role_entry)
                                second_third_relationship_score = self.relationship_score(second_role_entry,
                                                                                          third_role_entry)
                                tuple.add_pair(second_third_relationship_score, second_role_entry, third_role_entry)
                                entry_tuple_set.add(tuple)

        pattern_instance_list = []

        if len(entry_tuple_set) > 0:
            max_relationship_score = max(entry_tuple_set,
                                         key=lambda x: x.get_relationship_score()).get_relationship_score()
            for tuple in entry_tuple_set:
                if tuple.get_relationship_score() == max_relationship_score and tuple.get_relationship_score() > 0:
                    role_entries = tuple.get_role_entries()
                    instance = PatternInstance()
                    is_second_role = self.determine_actual_role_for_dual_pattern(role_entries)
                    for role_entry in role_entries:
                        if "/" in role_entry.get_role():
                            role_names = role_entry.get_role().split("/")
                            first_role_name = role_names[0]
                            second_role_name = role_names[1]
                            if is_second_role:
                                instance.add_entry(
                                    piEntry(RoleType.CLASS, second_role_name, role_entry.get_class_name(),
                                            role_entry.get_position()))
                                is_second_role = True
                            else:
                                instance.add_entry(
                                    piEntry(RoleType.CLASS, first_role_name, role_entry.get_class_name(),
                                            role_entry.get_position()))
                        else:
                            instance.add_entry(
                                piEntry(RoleType.CLASS, role_entry.get_role(), role_entry.get_class_name(),
                                        role_entry.get_position()))
                    for i in range(len(role_entries)):
                        role_entry1 = role_entries[i]
                        for j in range(i + 1, len(role_entries)):
                            role_entry2 = role_entries[j]
                            merge_output = self.merge_behavioral_data(role_entry1, role_entry2)
                            if self.pattern_descriptor.get_field_role_name() is not None:
                                fields = merge_output[0]
                                for field in fields:
                                    if "/" in self.pattern_descriptor.get_field_role_name():
                                        role_names = self.pattern_descriptor.get_field_role_name().split("/")
                                        first_role_name = role_names[0]
                                        second_role_name = role_names[1]
                                        if is_second_role:
                                            instance.add_entry(
                                                piEntry(RoleType.FIELD, second_role_name, field.get_signature(), -1))
                                        else:
                                            instance.add_entry(
                                                piEntry(RoleType.FIELD, first_role_name, field, -1))
                                    else:
                                        instance.add_entry(piEntry(RoleType.FIELD,
                                                                   self.pattern_descriptor.get_field_role_name(),
                                                                   field.get_signature(), -1))
                            if self.pattern_descriptor.get_method_role_name() is not None:
                                methods = merge_output[1]
                                for method in methods:
                                    if "/" in self.pattern_descriptor.get_method_role_name():
                                        role_names = self.pattern_descriptor.get_method_role_name().split("/")
                                        first_role_name = role_names[0]
                                        second_role_name = role_names[1]
                                        if is_second_role:
                                            instance.add_entry(piEntry(RoleType.METHOD, second_role_name,
                                                                       str(method.get_signature()), -1))
                                        else:
                                            instance.add_entry(piEntry(RoleType.METHOD, first_role_name,
                                                                       str(method.get_signature()), -1))
                                    else:
                                        instance.add_entry(piEntry(RoleType.METHOD,
                                                                   self.pattern_descriptor.get_method_role_name(),
                                                                   str(method.get_signature()), -1))

                    pattern_instance_list.append(instance)

        return pattern_instance_list

    def determine_actual_role_for_dual_pattern(self, role_entries):
        # special handling for distinguishing dual patterns, such as Adapter from Command
        for role_entry in role_entries:
            if "/" in role_entry.get_role():
                role_names = role_entry.get_role().split("/")
                second_role_name = role_names[1]
                if self.match(second_role_name, role_entry.get_class_name()):
                    return True
        return False

    def humanise(self, camel_case_string):
        return re.sub('([A-Z])', r' \1', camel_case_string)

    def match(self, role_name, actual_name):
        camel_case_tokens = self.humanise(role_name).split()
        for camel_case_token in camel_case_tokens:
            lower_case_token = camel_case_token.lower()
            if lower_case_token in actual_name.lower():
                return True
        return False

    # TODO da aggiungere tutte le matrici
    def relationship_score(self, e1, e2):
        score = 0
        if not isinstance(self.pattern_descriptor.get_association_matrix(), str):
            matrix = self.system_container.get_association_matrix()
            if matrix.iloc[e1.get_position(), e2.get_position()] == 1.0 or matrix.iloc[
                e2.get_position(), e1.get_position()] == 1.0:
                score += 1
        if not isinstance(self.pattern_descriptor.get_generalization_matrix(), str):
            matrix = self.system_container.get_generalization_matrix()
            if matrix.iloc[e1.get_position(), e2.get_position()] == 1.0 or matrix.iloc[
                e2.get_position(), e1.get_position()] == 1.0:
                score += 1
        if not isinstance(self.pattern_descriptor.get_invoked_method_in_inherited_method_matrix(), str):
            matrix = self.system_container.get_invoked_method_in_inherited_method_matrix()
            if matrix.iloc[e1.get_position(), e2.get_position()] == 1.0 or matrix.iloc[
                e2.get_position(), e1.get_position()] == 1.0:
                score += 1
        return score

    # TODO da aggiungere tutte le matrici
    def merge_behavioral_data(self, e1, e2):
        fields = set()
        methods = set()
        # if self.pattern_descriptor.get_iterative_similar_abstract_method_invocation_matrix() is not None:
        #    iterative_similar_abstract_method_invocation_behavioral_data = self.system_container.get_iterative_similar_abstract_method_invocation_behavioral_data()
        #    self.process_behavioral_data(iterative_similar_abstract_method_invocation_behavioral_data, e1, e2, fields,
        #                                 methods)

        if not isinstance(self.pattern_descriptor.get_invoked_method_in_inherited_method_matrix(), str):
            invoked_method_in_inherited_method_behavioral_data = self.system_container.get_invoked_method_in_inherited_method_behavioral_data()
            self.process_behavioral_data(invoked_method_in_inherited_method_behavioral_data, e1, e2, fields, methods)
        return fields, methods

    def process_behavioral_data(self, behavioral_data, e1, e2, fields, methods):
        fields1 = behavioral_data.get_fields(e1.get_position(), e2.get_position())
        if fields1 is not None:
            fields.update(fields1)
        if e1.get_position() != e2.get_position():
            fields2 = behavioral_data.get_fields(e2.get_position(), e1.get_position())
            if fields2 is not None:
                fields.update(fields2)
        methods1 = behavioral_data.get_methods(e1.get_position(), e2.get_position())
        if methods1 is not None:
            methods.update(methods1)
        if e1.get_position() != e2.get_position():
            methods2 = behavioral_data.get_methods(e2.get_position(), e1.get_position())
            if methods2 is not None:
                methods.update(methods2)


class Entry:
    score = ""
    role = ""
    class_name = ""
    position = ""
    hash = ""

    def __init__(self, score, role, class_name, position):
        self.score = score
        self.role = role
        self.class_name = class_name
        self.position = position
        self.hash = None

    def get_score(self):
        return self.score

    def get_role(self):
        return self.role

    def get_class_name(self):
        return self.class_name

    def get_position(self):
        return self.position

    def __eq__(self, other):
        if isinstance(other, Entry):
            return self.score == other.score and self.role == other.role and self.class_name == other.class_name
        return False

    def __lt__(self, other):
        if not self.score == other.score:
            return self.score < other.score
        if not self.role == other.role:
            return self.role < other.role
        return self.class_name < other.class_name

    def __hash__(self):
        if self.hash is None:
            self.hash = 17
            self.hash = 37 * self.hash + hash(self.score)
            self.hash = 37 * self.hash + hash(self.role)
            self.hash = 37 * self.hash + hash(self.class_name)
        return self.hash

    def __str__(self):
        return str(self.score) + " (" + self.role + "," + self.class_name + ")"


class EntryTuple:
    relationship_score = 0
    role_entries = list()
    hash_code = 0

    def __init__(self):
        self.relationship_score = 0
        self.role_entries = list()
        self.hash_code = 0

    def get_relationship_score(self):
        return self.relationship_score

    def get_role_entries(self):
        return self.role_entries

    def add_pair(self, relationship_score, e1, e2):
        if e1 not in self.role_entries:
            self.role_entries.append(e1)
        if e2 not in self.role_entries:
            self.role_entries.append(e2)
        self.relationship_score += relationship_score

    def __eq__(self, o):
        if isinstance(o, EntryTuple):
            if self.relationship_score != o.relationship_score:
                return False
            for e in o.role_entries:
                if e not in self.role_entries:
                    return False
            return True
        return False

    def __hash__(self):
        if self.hash_code == 0:
            result = 17
            result = 37 * result + self.relationship_score
            for e in self.role_entries:
                result = 37 * result + hash(e)
            self.hash_code = result
        return self.hash_code

    def __str__(self):
        return str(self.relationship_score) + " " + str(self.role_entries)

    def __lt__(self, o):
        if self.relationship_score != o.relationship_score:
            return self.relationship_score < o.relationship_score
        if len(self.role_entries) == len(o.role_entries):
            for i in range(len(self.role_entries)):
                if self.role_entries[i] != o.role_entries[i]:
                    return self.role_entries[i] < o.role_entries[i]
        else:
            return len(self.role_entries) < len(o.role_entries)
        return False
