class InheritanceHierarchy:

    root_node = {}

    def __init__(self):
        self.root_node = None

    def get_node(self, node_name):
        if self.root_node is not None:
            for node in self.breadth_first_enumeration(self.root_node):
                if node['userObject'] == node_name:
                    return node
        return None

    def add_child_to_parent(self, child_node, parent_node):
        c_node = self.get_node(child_node)
        if c_node is None:
            c_node = {'userObject': child_node, 'children': []}
        p_node = self.get_node(parent_node)
        if p_node is None:
            p_node = {'userObject': parent_node, 'children': []}
            self.root_node = p_node
        p_node['children'].append(c_node)

    def add_child_root_node_to_parent(self, child_root_node, parent_node):
        p_node = self.get_node(parent_node)
        if p_node is None:
            p_node = {'userObject': parent_node, 'children': []}
            self.root_node = p_node
        p_node['children'].append(child_root_node)

    def deep_clone(self, root):
        n_root = root.copy()
        n_root['children'] = []
        for child in root['children']:
            n_child = self.deep_clone(child)
            n_root['children'].append(n_child)
        return n_root

    def equals(self, o):
        if self is o:
            return True
        if isinstance(o, InheritanceHierarchy):
            return self.root_node['userObject'] == o.root_node['userObject']
        return False

    def get_root_node(self):
        return self.root_node

    def get_enumeration(self):
        return self.breadth_first_enumeration(self.root_node)

    def size(self):
        return len(list(self.breadth_first_enumeration(self.root_node)))

    def __str__(self):
        return str(self.root_node['userObject'])

    @staticmethod
    def breadth_first_enumeration(node):
        nodes = [node]
        for node in nodes:
            yield node
            if 'children' in node:
                nodes.extend(node['children'])
