class ImportsDetector:
    imports_list = {}

    def __init__(self, system_object):
        self.detect_all_imports(system_object)

    def detect_all_imports(self, system_object):
        for i in range(system_object.get_class_number()):
            class_or_file_object = system_object.get_class_object_with_position(i)
            key = class_or_file_object.get_class_name()
            if class_or_file_object.get_file_name() != "":
                key = class_or_file_object.get_file_name() + "." + key
            if key not in self.imports_list:
                self.imports_list[key] = list()
            for import_ in class_or_file_object.get_imports_list():
                self.imports_list[key].append(import_)
            for function in class_or_file_object.get_functions_list():
                for import_ in function.get_imports_list():
                    self.imports_list[key].append(import_)
                    class_or_file_object.add_import(import_)
                    function.remove_import(import_)

    def control_an_import(self, class_name):
        for key in self.imports_list:
            for import_ in self.imports_list[key]:
                for import_from_list in import_.get_import_list():
                    if import_from_list == class_name:
                        split = import_.get_from_name().split(".")
                        return split[len(split) - 1]
        return None
