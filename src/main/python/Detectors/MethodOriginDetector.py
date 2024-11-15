from Downloader.ProgressionCheck import ProgressDetection
from Objects.CallFunctionObject import CallFunctionObject
from Objects.VariableObject import VariableObject


class MethodOriginDetector:
    functions_list = {}
    progressor = ProgressDetection()

    def __init__(self, system_object, terminal):
        self.progressor = ProgressDetection()
        self.functions_list = {}
        self.take_all_functions(system_object, terminal)
        self.detect_call_function_origin(system_object, terminal)

    def take_all_functions(self, system_object, terminal):
        for i in range(system_object.get_class_number()):
            self.progressor.update(len(system_object.get_class_names()), i, "MethodOriginDetector take all functions",
                                   terminal)
            class_or_file_object = system_object.get_class_object_with_position(i)
            class_name = class_or_file_object.get_class_name()
            file_name = class_or_file_object.get_file_name()
            key = file_name + "." + class_name
            if file_name is None or file_name == "":
                key = class_name
            if key not in self.functions_list:
                self.functions_list[key] = list()
            for function in class_or_file_object.get_functions_list():
                self.functions_list[key].append(function.get_function_name())

    def detect_call_function_origin(self, system_object, terminal):
        for i in range(system_object.get_class_number()):
            self.progressor.update(len(system_object.get_class_names()), i,
                                   "MethodOriginDetector detect call function origins", terminal)
            class_or_file_object = system_object.get_class_object_with_position(i)
            for function in class_or_file_object.get_functions_list():
                for instruction in function.get_instructions_list():
                    if isinstance(instruction, VariableObject):
                        if isinstance(instruction.get_argument(), CallFunctionObject):
                            candidate_classes = list()
                            for class_of_function_list in self.functions_list:
                                for function_of_class in self.functions_list[class_of_function_list]:
                                    if function_of_class == str(
                                            instruction.get_argument().get_method_name()).removeprefix(
                                            "."):
                                        candidate_classes.append(class_of_function_list)
                            if 0 < len(candidate_classes) < 2:
                                instruction.get_argument().set_original_class_name(candidate_classes[0])
                    elif isinstance(instruction, CallFunctionObject):
                        candidate_classes = list()
                        for class_of_function_list in self.functions_list:
                            for function_of_class in self.functions_list[class_of_function_list]:
                                if isinstance(instruction.get_method_name(), int):
                                    continue
                                elif instruction.get_method_name() is None:
                                    continue
                                if function_of_class == str(instruction.get_method_name()).removeprefix("."):
                                    candidate_classes.append(class_of_function_list)
                        if 0 < len(candidate_classes) < 2:
                            instruction.set_original_class_name(candidate_classes[0])
                if isinstance(function.get_return_object().get_argument(), CallFunctionObject):
                    candidate_classes = list()
                    for class_of_function_list in self.functions_list:
                        for function_of_class in self.functions_list[class_of_function_list]:
                            if function_of_class == str(function.get_return_object().get_argument() \
                                    .get_method_name()).removeprefix("."):
                                candidate_classes.append(class_of_function_list)
                    if 0 < len(candidate_classes) < 2:
                        function.get_return_object().get_argument().set_original_class_name(candidate_classes[0])
            for instruction in class_or_file_object.get_instructions_list():
                if isinstance(instruction, VariableObject):
                    if isinstance(instruction.get_argument(), CallFunctionObject):
                        candidate_classes = list()
                        for class_of_function_list in self.functions_list:
                            for function_of_class in self.functions_list[class_of_function_list]:
                                if function_of_class == str(instruction.get_argument().get_method_name()).removeprefix(
                                        "."):
                                    candidate_classes.append(class_of_function_list)
                        if 0 < len(candidate_classes) < 2:
                            instruction.get_argument().set_original_class_name(candidate_classes[0])
                elif isinstance(instruction, CallFunctionObject):
                    candidate_classes = list()
                    for class_of_function_list in self.functions_list:
                        for function_of_class in self.functions_list[class_of_function_list]:
                            if function_of_class == str(instruction.get_method_name()).removeprefix("."):
                                candidate_classes.append(class_of_function_list)
                    if 0 < len(candidate_classes) < 2:
                        instruction.set_original_class_name(candidate_classes[0])
