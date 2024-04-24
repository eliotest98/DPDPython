from typing import Iterable

from bytecode import CellVar

from Downloader.ProgressionCheck import ProgressDetection
from Objects.CallFunctionObject import CallFunctionObject
from Objects.CicleObject import CicleObject
from Objects.ClassObject import ClassObject
from Objects.ExceptionObject import ExceptionObject
from Objects.FileObject import FileObject
from Objects.IfObject import IfObject
from Objects.ImportObject import ImportObject
from Objects.OperationObject import OperationObject
from Objects.ReturnObject import ReturnObject
from Objects.VariableObject import VariableObject


# This class detect the superclasses of a specific class
class SuperclassDetector:
    functions_list_of_classes = {}
    progressor = ProgressDetection()

    def __init__(self, system_object, terminal):
        self.progressor = ProgressDetection()
        self.functions_list_of_classes = {}
        self.get_all_functions(system_object, terminal)
        self.detect_with_functions(system_object, terminal)
        self.adjust_superclass(system_object, terminal)

    def get_all_functions(self, system_object, terminal):
        for i in range(system_object.get_class_number()):
            self.progressor.update(len(system_object.get_class_names()), i, "SuperclassDetector get all functions",
                                   terminal)
            class_object = system_object.get_class_object_with_position(i)
            if isinstance(class_object, FileObject):
                for single_class in class_object.get_class_list():
                    key = single_class.get_file_name() + "." + single_class.get_class_name()
                    for function_object in single_class.get_functions_list():
                        if key not in self.functions_list_of_classes:
                            self.functions_list_of_classes[key] = list()
                        self.functions_list_of_classes[key].append(function_object.get_function_name())

    def detect_with_functions(self, system_object, terminal):
        for i in range(system_object.get_class_number()):
            self.progressor.update(len(system_object.get_class_names()), i, "SuperclassDetector detect with functions",
                                   terminal)
            class_object = system_object.get_class_object_with_position(i)
            if isinstance(class_object, FileObject):
                for single_class in class_object.get_class_list():
                    for function_object in single_class.get_functions_list():
                        method_name = self.recursive_detection(function_object.get_instructions_list())
                        if method_name is not None:
                            method_name = method_name.removeprefix(".")
                            for class_name, methods_list in self.functions_list_of_classes.items():
                                for inside_method in methods_list:
                                    if inside_method == method_name:
                                        single_class.add_superclass(class_name)
                        # This is for the return
                        if isinstance(function_object.get_return_object().get_argument(), CallFunctionObject):
                            method_name = function_object.get_return_object().get_argument().get_method_name()
                            if method_name is not None:
                                if isinstance(method_name, (VariableObject, CallFunctionObject)):
                                    method_name = str(method_name)
                                method_name = str(method_name).removeprefix(".")
                                for class_name, methods_list in self.functions_list_of_classes.items():
                                    for inside_method in methods_list:
                                        if inside_method == method_name:
                                            single_class.add_superclass(class_name)

    def recursive_detection(self, list_):
        if isinstance(list_, CallFunctionObject):
            return list_.get_method_name()
        elif isinstance(list_, VariableObject):
            self.recursive_detection(list_.get_argument())
        elif isinstance(list_, IfObject):
            self.recursive_detection(list_.get_instruction_list_true())
            self.recursive_detection(list_.get_instruction_list_false())
        elif isinstance(list_, ExceptionObject):
            self.recursive_detection(list_.get_instruction_list_try())
            self.recursive_detection(list_.get_instruction_list_except())
        elif isinstance(list_, (CicleObject, ReturnObject, ImportObject, OperationObject)):
            pass
        elif isinstance(list_, (int, str, float, CellVar)):
            pass
        elif list_ is None:
            pass
        else:
            if isinstance(list_, Iterable):
                for instruction in list_:
                    self.recursive_detection(instruction)

    # This function adjust the path of superclasses detected
    def adjust_superclass(self, system_object, terminal):
        for i in range(system_object.get_class_number()):
            self.progressor.update(len(system_object.get_class_names()), i, "SuperclassDetector adjust superclass",
                                   terminal)
            class_object = system_object.get_class_object_with_position(i)
            if isinstance(class_object, ClassObject):
                list_to_delete = list()
                list_to_add = list()
                for superclass in class_object.get_superclass_list():
                    key_found = ""
                    for key in self.functions_list_of_classes.keys():
                        # split = key.split(".")
                        # if split[len(split) - 1] == superclass:
                        #     key_found = key
                        #     break
                        if key == superclass:
                            key_found = key
                            break
                        # Control if the class is in the same file
                        else:
                            key_to_control = class_object.get_file_name() + "." + superclass
                            if key == key_to_control:
                                key_found = key
                                break
                    if key_found == "":
                        list_to_delete.append(superclass)
                        list_to_add.append("Import:" + superclass)
                    else:
                        list_to_delete.append(superclass)
                        list_to_add.append(key_found)

                for import_ in list_to_delete:
                    class_object.remove_superclass(import_)

                for import_ in list_to_add:
                    class_object.add_superclass(import_)
