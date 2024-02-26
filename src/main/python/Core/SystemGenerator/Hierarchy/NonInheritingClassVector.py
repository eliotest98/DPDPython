class NonInheritingClassVector:

    non_inheriting_classes = list()

    def __init__(self):
        self.non_inheriting_classes = []

    def get_node(self, node_name):
        for node in self.non_inheriting_classes:
            if node['userObject'] == node_name:
                return node
        return None

    def add(self, node):
        self.non_inheriting_classes.append(node)

    def get_enumeration(self):
        return iter(self.non_inheriting_classes)

    def size(self):
        return len(self.non_inheriting_classes)

    def equals(self, ih):
        return False

    def __str__(self):
        if self.non_inheriting_classes:
            return str(self.non_inheriting_classes[0]['userObject'])
        else:
            return None
