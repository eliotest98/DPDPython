class Entry:

    hierarchy_list = list()
    number_of_method_invocations = 0

    def __init__(self):
        self.hierarchy_list = list()
        self.number_of_method_invocations = 0

    def add_hierarchy(self, ih):
        self.hierarchy_list.append(ih)

    def set_number_of_method_invocations(self, n):
        self.number_of_method_invocations = n

    def get_number_of_method_invocations(self):
        return self.number_of_method_invocations

    def get_hierarchy_list(self):
        return self.hierarchy_list

    def __eq__(self, other):
        if isinstance(other, Entry):
            return self.number_of_method_invocations == other.number_of_method_invocations and self.hierarchy_list == other.hierarchy_list
        return False

    def __hash__(self):
        return hash((self.number_of_method_invocations, tuple(self.hierarchy_list)))

    def __str__(self):
        return str(self.number_of_method_invocations) + " " + str(self.hierarchy_list)


class ClusterSet:

    entry_set = set()

    def __init__(self):
        self.entry_set = set()

    def add_cluster_entry(self, e):
        self.entry_set.add(e)

    def get_cluster_set(self):
        return sorted(list(self.entry_set), key=lambda x: x.get_number_of_method_invocations(), reverse=True)
