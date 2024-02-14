class HierarchyDetection:

    hierarchy_list = list()

    def __init__(self, system_object):
        # Is a way to define a hereditary class
        superclass_list = ""

    def get_superclass_hierarchy_list(self, system_object):
        superclass_list = list()
        for file_object in system_object.get_file_list():
            for class_object in file_object.get_class_list():
                print("")
