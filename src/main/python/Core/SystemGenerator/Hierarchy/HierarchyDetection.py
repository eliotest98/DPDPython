from Core.SystemGenerator.Hierarchy.InheritanceHierarchy import InheritanceHierarchy
from Core.SystemGenerator.Hierarchy.NonInheritingClassVector import NonInheritingClassVector
from Objects.FileObject import FileObject


class HierarchyDetection:
    hierarchy_list = list()

    def __init__(self, system_object):
        # Is a way to define a hereditary class
        self.hierarchy_list = self.get_superclass_hierarchy_list(system_object)
        self.get_non_inheriting_classes(system_object)

    def get_hierarchy_list(self):
        return self.hierarchy_list

    def get_non_inheriting_classes(self, system_object):
        non_inheriting_class = NonInheritingClassVector()
        for i in range(system_object.get_class_number()):
            file_object = system_object.get_class_object_with_position(i)
            if isinstance(file_object, FileObject):
                for class_object in file_object.get_class_list():
                    if self.get_hierarchy(self.hierarchy_list, class_object.get_class_name()) is None:
                        non_inheriting_class.add(class_object.get_class_name())
        self.hierarchy_list.append(non_inheriting_class)

    def get_superclass_hierarchy_list(self, system_object):
        superclass_list = list()
        for i in range(system_object.get_class_number()):
            file_object = system_object.get_class_object_with_position(i)
            if isinstance(file_object, FileObject):
                for class_object in file_object.get_class_list():
                    if len(class_object.get_superclass_list()) != 0:
                        child_hierarchy = self.get_hierarchy(superclass_list, class_object.get_class_name())
                        for parent in class_object.get_superclass_list():
                            parent_hierarchy = self.get_hierarchy(superclass_list, parent)
                            if child_hierarchy is None and parent_hierarchy is None:
                                ih = InheritanceHierarchy()
                                ih.add_child_to_parent(class_object.get_class_name(), parent)
                                superclass_list.append(ih)
                            elif child_hierarchy is None:
                                parent_hierarchy.add_child_to_parent(class_object.get_class_name(), parent)
                            elif parent_hierarchy is None:
                                child_hierarchy.add_child_to_parent(class_object.get_class_name(), parent)
                            elif child_hierarchy.equals(parent_hierarchy):
                                parent_hierarchy.add_child_root_node_to_parent(child_hierarchy.get_root_node(), parent)
                                superclass_list.remove(child_hierarchy)
        return superclass_list

    def get_hierarchy(self, hierarchy_list, node_name):
        for enum in hierarchy_list:
            if enum.get_node(node_name) is not None:
                return enum
        return None