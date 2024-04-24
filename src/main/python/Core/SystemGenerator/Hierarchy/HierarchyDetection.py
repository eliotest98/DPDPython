from Core.SystemGenerator.Hierarchy.InheritanceHierarchy import InheritanceHierarchy
from Core.SystemGenerator.Hierarchy.NonInheritingClassVector import NonInheritingClassVector
from Downloader.ProgressionCheck import ProgressDetection
from Objects.FileObject import FileObject


class HierarchyDetection:
    hierarchy_list = list()
    progressor = ProgressDetection()

    def __init__(self, system_object,terminal):
        self.hierarchy_list = list()
        self.progressor = ProgressDetection()
        # Is a way to define a hereditary class
        self.hierarchy_list = self.get_superclass_hierarchy_list(system_object,terminal)
        self.get_non_inheriting_classes(system_object,terminal)

    def get_hierarchy_list(self):
        return self.hierarchy_list

    def get_non_inheriting_classes(self, system_object,terminal):
        non_inheriting_class = NonInheritingClassVector()
        for i in range(system_object.get_class_number()):
            self.progressor.update(len(system_object.get_class_names()), i, "HierarchyDetector get non inheriting classes",terminal)
            file_object = system_object.get_class_object_with_position(i)
            if isinstance(file_object, FileObject):
                for class_object in file_object.get_class_list():
                    key = class_object.get_class_name()
                    if class_object.get_file_name() != "":
                        key = class_object.get_file_name() + "." + key
                    if self.get_hierarchy(self.hierarchy_list, key) is None:
                        non_inheriting_class.add(key)
        self.hierarchy_list.append(non_inheriting_class)

    def get_superclass_hierarchy_list(self, system_object,terminal):
        superclass_list = list()
        for i in range(system_object.get_class_number()):
            self.progressor.update(len(system_object.get_class_names()), i, "HierarchyDetector get superclass hierarchy list",terminal)
            file_object = system_object.get_class_object_with_position(i)
            if isinstance(file_object, FileObject):
                for class_object in file_object.get_class_list():
                    key = class_object.get_class_name()
                    if class_object.get_file_name() != "":
                        key = class_object.get_file_name() + "." + key
                    if len(class_object.get_superclass_list()) != 0:
                        child_hierarchy = self.get_hierarchy(superclass_list, key)
                        for parent in class_object.get_superclass_list():
                            if parent.__contains__(":"):
                                split = parent.split(":")
                                if split[0] == "Import":
                                    continue
                            parent_hierarchy = self.get_hierarchy(superclass_list, parent)
                            if child_hierarchy is None and parent_hierarchy is None:
                                ih = InheritanceHierarchy()
                                ih.add_child_to_parent(key, parent)
                                superclass_list.append(ih)
                            elif child_hierarchy is None:
                                parent_hierarchy.add_child_to_parent(key, parent)
                            elif parent_hierarchy is None:
                                child_hierarchy.add_child_to_parent(key, parent)
                            elif child_hierarchy.equals(parent_hierarchy):
                                parent_hierarchy.add_child_root_node_to_parent(child_hierarchy.get_root_node(), parent)
                                superclass_list.remove(child_hierarchy)
        return superclass_list

    def get_hierarchy(self, hierarchy_list, node_name):
        for enum in hierarchy_list:
            if enum.get_node(node_name) is not None:
                return enum
        return None