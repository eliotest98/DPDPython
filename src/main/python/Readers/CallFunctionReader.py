import html

from bytecode import Label, Instr
from bytecode import bytecode
from Objects.CallFunctionObject import CallFunctionObject
from Objects.CicleObject import CicleObject
from Objects.FunctionObject import FunctionObject
from Objects.OperationObject import OperationObject
from Objects.VariableObject import VariableObject


class CallFunctionReader:

    def read_call_function(self, call_function_object, bytecode_instructions, debug_active):
        if debug_active == 1:
            print("\n" + call_function_object.method_name + " Call Function Reading...")
        # Copy for delete instructions when visited
        by = bytecode_instructions

        # Instruction Counter
        i = 0

        # List the instructions
        while i < len(by):
            instruction = by[i]
            if debug_active == 1:
                print(instruction)
            match instruction.name:

                # CallMethod -> LOAD_NAME LOAD_METHOD CALL_METHOD
                # CallMethod -> LOAD_NAME LOAD_ATTR LOAD_METHOD CALL_METHOD
                case "CALL_METHOD":
                    number_of_args = instruction.arg
                    i = i + 1
                    count = 0
                    # Parameters
                    while count < number_of_args:
                        if isinstance(by[i], Label):
                            return ""
                        elif by[i].name == "LOAD_CONST":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(
                                str(type(return_values[0]).__name__) + ":" + str(return_values[0]))
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "LOAD_NAME":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "BUILD_MAP":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "CALL_METHOD":
                            return_values = self.recursive_identification(by[i:])
                            by = return_values[1]
                            i = 0
                            call_function_object.add_parameter(return_values[0])
                            count = count + 1
                        elif by[i].name.__contains__("_OP"):
                            return_values = self.recursive_identification(by[i:])
                            by = return_values[1]
                            i = 0
                            call_function_object.add_parameter(return_values[0])
                            count = count + 1
                        elif by[i].name == "BINARY_SUBTRACT":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "BUILD_CONST_KEY_MAP":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        # BodyFunction -> CallFunction
                        elif by[i].name == "CALL_FUNCTION":
                            return_values = self.recursive_identification(by[i:])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                            call_function_object.add_parameter(return_values[0])
                        elif by[i].name == "CALL_FUNCTION_KW":
                            return_values = self.recursive_identification(by[i:])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                            call_function_object.add_parameter(return_values[0])
                        # BodyFunction -> Cicle
                        # BodyFunction -> BINARY_SUBSCR
                        # BodyFunction -> BINARY_ADD
                        # BodyFunction -> BUILD_LIST
                        # BodyFunction -> LOAD_GLOBAL
                        # BodyFunction -> LOAD_ATTR
                        # BodyFunction -> LOAD_FAST
                        elif by[i].name == "GET_ITER" or by[i].name == "BINARY_ADD" or by[i].name == "BINARY_SUBSCR" \
                                or by[i].name == "BUILD_LIST" or by[i].name == "LOAD_GLOBAL" \
                                or by[i].name == "LOAD_ATTR" or by[i].name == "LOAD_FAST" \
                                or by[i].name == "BINARY_MODULO" or by[i].name == "BINARY_MULTIPLY" \
                                or by[i].name == "BINARY_TRUE_DIVIDE" or by[i].name == "LIST_EXTEND" \
                                or by[i].name == "BINARY_POWER" or by[i].name == "MAKE_FUNCTION" \
                                or by[i].name == "BUILD_TUPLE" or by[i].name == "LOAD_DEREF" \
                                or by[i].name == "MAKE_FUNCTION" or by[i].name == "BUILD_SLICE" \
                                or by[i].name == "LIST_APPEND" or by[i].name == "BUILD_STRING" \
                                or by[i].name == "BINARY_AND" or by[i].name == "BINARY_OR" \
                                or by[i].name == "UNARY_INVERT" or by[i].name == "BUILD_SET" \
                                or by[i].name == "UNARY_NEGATIVE" or by[i].name == "SET_UPDATE" \
                                or by[i].name == "CALL_FUNCTION_EX":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "LOAD_METHOD":
                            break
                        else:
                            print("ERROR PARAMETERS CALL_METHOD")
                            print(by[i])
                            exit(-1)

                    # Skipping...
                    if isinstance(by[i], Label):
                        i = i + 1
                        while by[i].name != "LOAD_METHOD":
                            i = i + 1
                            if isinstance(by[i], Label):
                                i = i + 1

                    if by[i].name == "LOAD_METHOD":
                        call_function_object.set_method_name("." + by[i].arg)
                        i = i + 1

                    if isinstance(by[i], Label):
                        return ""

                    if by[i].name == "LOAD_NAME":
                        path = call_function_object.path
                        if path == "":
                            path = by[i].arg
                        else:
                            if path.endswith("."):
                                path = path + by[i].arg
                            else:
                                path = path + "." + by[i].arg
                        call_function_object.set_path(path)
                        return by[i:]
                    if by[i].name == "LOAD_FAST":
                        path = call_function_object.path
                        if path == "":
                            path = by[i].arg
                        else:
                            if path.endswith("."):
                                path = path + by[i].arg
                            else:
                                path = path + "." + by[i].arg
                        call_function_object.set_path(path)
                        return by[i:]
                    # CallMethod -> CallMethod.CallMethod
                    elif by[i].name == "CALL_METHOD":
                        # Create a Call Function Object
                        return_values = self.recursive_identification(by[i:])
                        by = return_values[1]
                        i = 0
                        count = count + 1
                        call_function_object.add_parameter(return_values[0])
                    # CallMethod -> LOAD_NAME LOAD_ATTR LOAD_METHOD CALL_METHOD
                    elif by[i].name == "LOAD_ATTR":
                        return_values = self.recursive_identification(by[i:])
                        path = call_function_object.path
                        if path == "":
                            path = return_values[0]
                        else:
                            if path.endswith("."):
                                path = path + return_values[0]
                            else:
                                path = path + "." + return_values[0]
                        call_function_object.set_path(path)
                        return return_values[1]
                    # CallMethod -> CallMethod.CallFunction
                    elif by[i].name == "CALL_FUNCTION":
                        internal_call_method = CallFunctionObject()
                        fun_name = self.read_call_function(internal_call_method, by[i:], debug_active)
                        call_function_object.add_concat(internal_call_method)
                        return fun_name
                    elif by[i].name == "CALL_FUNCTION_KW":
                        internal_call_method = CallFunctionObject()
                        fun_name = self.read_call_function(internal_call_method, by[i:], debug_active)
                        call_function_object.add_concat(internal_call_method)
                        return fun_name
                    # CallMethod -> LOAD_GLOBAL LOAD_ATTR LOAD_METHOD CALL_METHOD
                    elif by[i].name == "LOAD_GLOBAL":
                        path = call_function_object.path
                        if path == "":
                            path = by[i].arg
                        else:
                            if path.endswith("."):
                                path = path + by[i].arg
                            else:
                                path = path + "." + by[i].arg
                        call_function_object.set_path(path)
                        return by[i:]
                    elif by[i].name == "BINARY_SUBSCR":
                        return_values = self.recursive_identification(by[i:])
                        path = call_function_object.path
                        if path == "":
                            path = return_values[0]
                        else:
                            if path.endswith("."):
                                path = path + return_values[0]
                            else:
                                path = path + "." + return_values[0]
                        call_function_object.set_path(path)
                        return return_values[1]
                    elif by[i].name == "LOAD_CONST":
                        return by[i].arg
                    elif by[i].name == "LOAD_DEREF":
                        return by[i].arg
                    elif by[i].name == "BUILD_TUPLE":
                        return_values = self.recursive_identification(by[i:])
                        return return_values[1]
                    elif by[i].name.__contains__("_OP"):
                        return_values = self.recursive_identification(by[i:])
                        call_function_object.add_concat(return_values[0])
                        return return_values[1]
                    elif by[i].name == "BINARY_MULTIPLY":
                        return_values = self.recursive_identification(by[i:])
                        call_function_object.add_concat(return_values[0])
                        return return_values[1]
                    elif by[i].name == "BINARY_SUBTRACT":
                        return_values = self.recursive_identification(by[i:])
                        call_function_object.add_concat(return_values[0])
                        return return_values[1]
                    elif by[i].name == "BINARY_OR":
                        return_values = self.recursive_identification(by[i:])
                        call_function_object.add_concat(return_values[0])
                        return return_values[1]
                    elif by[i].name == "LIST_EXTEND":
                        return_values = self.recursive_identification(by[i:])
                        call_function_object.add_concat(return_values[0])
                        return return_values[1]
                    elif by[i].name == "STORE_FAST":
                        return_values = self.recursive_identification(by[i:])
                        return return_values[1]
                    elif by[i].name == "BUILD_STRING":
                        return_values = self.recursive_identification(by[i:])
                        return return_values[1]
                    else:
                        print("ERROR CALL_METHOD")
                        print(by[i])

                # CallFunction -> LOAD_NAME BodyFunction CALL_FUNCTION
                case "CALL_FUNCTION":
                    number_of_args = instruction.arg
                    i = i + 1
                    count = 0
                    # Body Function
                    while count < number_of_args:
                        if isinstance(by[i], Label):
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        # BodyFunction -> LOAD_CONST
                        elif by[i].name == "LOAD_CONST":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(
                                str(type(return_values[0]).__name__) + ":" + str(return_values[0]))
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        # BodyFunction -> LOAD_NAME
                        elif by[i].name == "LOAD_NAME":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        # BodyFunction -> LOAD_FAST
                        elif by[i].name == "LOAD_FAST":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        # BodyFunction -> CallFunction
                        elif by[i].name == "CALL_FUNCTION":
                            return_values = self.recursive_identification(by[i:])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                            call_function_object.add_parameter(return_values[0])
                        elif by[i].name == "CALL_FUNCTION_KW":
                            return_values = self.recursive_identification(by[i:])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                            call_function_object.add_parameter(return_values[0])
                        # BodyFunction -> CallMethod
                        elif by[i].name == "CALL_METHOD":
                            # Create a Call Function Object
                            return_values = self.recursive_identification(by[i:])
                            by = return_values[1]
                            i = 0
                            call_function_object.add_parameter(return_values[0])
                            count = count + 1
                        # BodyFunction -> Cicle
                        elif by[i].name == "GET_ITER":
                            return_values = self.recursive_identification(by[i:])
                            # Add cicle at instructions of File Object
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        # BodyFunction -> BINARY_SUBSCR
                        elif by[i].name == "BINARY_SUBSCR":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        # BodyFunction -> BINARY_ADD
                        elif by[i].name == "BINARY_ADD":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "BUILD_LIST":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "BINARY_MODULO" or by[i].name == "BINARY_SUBTRACT" \
                                or by[i].name == "BUILD_MAP" or by[i].name == "LOAD_GLOBAL" \
                                or by[i].name == "LOAD_ATTR" or by[i].name == "LIST_EXTEND" \
                                or by[i].name == "BINARY_MULTIPLY" or by[i].name == "MAKE_FUNCTION" \
                                or by[i].name == "BINARY_TRUE_DIVIDE" or by[i].name == "BUILD_TUPLE" \
                                or by[i].name == "BUILD_CONST_KEY_MAP" or by[i].name == "BUILD_STRING" \
                                or by[i].name == "LOAD_DEREF" or by[i].name == "BINARY_FLOOR_DIVIDE" \
                                or by[i].name == "BINARY_OR" or by[i].name == "BINARY_AND" \
                                or by[i].name == "CALL_FUNCTION_EX" or by[i].name == "UNARY_NEGATIVE" \
                                or by[i].name == "UNARY_INVERT":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        else:
                            print("ERROR CALL_FUNCTION PARAMETERS")
                            print(by[i])

                    if i < len(by):
                        if isinstance(by[i], Label):
                            return call_function_object
                        if by[i].name == "LOAD_NAME":
                            call_function_object.set_method_name(by[i].arg)
                            return by[i]
                        elif by[i].name == "LOAD_GLOBAL":
                            call_function_object.set_method_name(by[i].arg)
                            return by[i]
                        elif by[i].name == "LOAD_CONST":
                            call_function_object.set_method_name(by[i].arg)
                            if by[i].arg.__contains__("<"):
                                temp = by[i].arg.removeprefix("<")
                                temp = temp.removesuffix(">")
                                by[i].arg = temp
                            return by[i]
                        elif by[i].name == "LOAD_FAST":
                            call_function_object.set_method_name(by[i].arg)
                            return by[i]
                        elif by[i].name == "STORE_NAME":
                            # This is the variable name
                            return by[i]
                        elif by[i].name == "STORE_FAST":
                            # This is the variable name
                            return by[i]
                        elif by[i].name == "BUILD_TUPLE":
                            return_values = self.recursive_identification(by[i:])
                            return return_values[0]
                        elif by[i].name == "LOAD_DEREF":
                            return_values = self.recursive_identification(by[i:])
                            return return_values[0]
                        elif by[i].name == "CALL_FUNCTION_KW":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_concat(return_values[0])
                            return call_function_object
                        elif by[i].name == "BINARY_SUBSCR":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_concat(return_values[0])
                            return call_function_object
                        elif by[i].name == "CALL_FUNCTION":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_concat(return_values[0])
                            return call_function_object
                        elif by[i].name == "BUILD_SLICE":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_concat(return_values[0])
                            return call_function_object
                        elif by[i].name == "CALL_METHOD":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_concat(return_values[0])
                            return call_function_object
                        elif by[i].name == "STORE_SUBSCR":
                            # Skipping...
                            return call_function_object
                        elif by[i].name == "LOAD_BUILD_CLASS":
                            # Skipping...
                            return call_function_object
                        elif by[i].name == "MAKE_FUNCTION":
                            # Skipping...
                            return call_function_object
                        else:
                            print("CALL_FUNCTION Call Function Reader not registered")
                            print(by[i])

                # CallFunction -> LOAD_NAME BodyFunction CALL_FUNCTION_KW
                case "CALL_FUNCTION_KW":
                    number_of_args = instruction.arg
                    i = i + 1
                    arguments_list = by[i].arg
                    i = i + 1
                    count = 0
                    # Body Function
                    while count < number_of_args:
                        # BodyFunction -> LOAD_CONST
                        if by[i].name == "LOAD_CONST":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(
                                str(type(return_values[0]).__name__) + ":" + str(return_values[0]))
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        # BodyFunction -> LOAD_NAME
                        elif by[i].name == "LOAD_NAME":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        # BodyFunction -> LOAD_FAST
                        elif by[i].name == "LOAD_FAST":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        # BodyFunction -> CallFunction
                        elif by[i].name == "CALL_FUNCTION":
                            return_values = self.recursive_identification(by[i:])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                            call_function_object.add_parameter(return_values[0])
                        # BodyFunction -> CallMethod
                        elif by[i].name == "CALL_METHOD":
                            # Create a Call Function Object
                            return_values = self.recursive_identification(by[i:])
                            by = return_values[1]
                            i = 0
                            call_function_object.add_parameter(return_values[0])
                            count = count + 1
                        # BodyFunction -> Cicle
                        elif by[i].name == "GET_ITER":
                            return_values = self.recursive_identification(by[i:])
                            # Add cicle at instructions of File Object
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        # BodyFunction -> BINARY_SUBSCR
                        elif by[i].name == "BINARY_SUBSCR":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        # BodyFunction -> BINARY_ADD
                        elif by[i].name == "BINARY_ADD":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "BINARY_SUBTRACT":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "LOAD_ATTR":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "LOAD_GLOBAL":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "BUILD_LIST":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "BUILD_MAP":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name.__contains__("_OP"):
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        elif by[i].name == "BINARY_MODULO" or by[i].name == "BINARY_TRUE_DIVIDE" \
                                or by[i].name == "BUILD_CONST_KEY_MAP" or by[i].name == "BINARY_MULTIPLY" \
                                or by[i].name == "BUILD_TUPLE" or by[i].name == "LOAD_DEREF" \
                                or by[i].name == "LIST_APPEND" or by[i].name == "LIST_EXTEND" \
                                or by[i].name == "CALL_FUNCTION_KW" or by[i].name == "MAKE_FUNCTION" \
                                or by[i].name == "CALL_FUNCTION_EX" or by[i].name == "BINARY_FLOOR_DIVIDE" \
                                or by[i].name == "BUILD_STRING" or by[i].name == "SET_UPDATE" \
                                or by[i].name == "BUILD_SET" or by[i].name == "MAP_ADD":
                            return_values = self.recursive_identification(by[i:])
                            call_function_object.add_parameter(return_values[0])
                            by = return_values[1]
                            i = 0
                            count = count + 1
                        else:
                            print("ERROR CALL_FUNCTION PARAMETERS KW")
                            print(by[i])

                    if i < len(by):
                        if isinstance(by[i], Label):
                            return ""
                        elif by[i].name == "LOAD_NAME":
                            call_function_object.set_method_name(by[i].arg)
                            return by[i]
                        elif by[i].name == "LOAD_GLOBAL":
                            call_function_object.set_method_name(by[i].arg)
                            return by[i]
                        elif by[i].name == "LOAD_CONST":
                            call_function_object.set_method_name(by[i].arg)
                            if by[i].arg.__contains__("<"):
                                temp = by[i].arg.removeprefix("<")
                                temp = temp.removesuffix(">")
                                by[i].arg = temp
                            return by[i]
                        elif by[i].name == "LOAD_FAST":
                            call_function_object.set_method_name(by[i].arg)
                            return by[i]
                        elif by[i].name == "LOAD_ATTR":
                            call_function_object.set_method_name(by[i].arg)
                            i = i + 1
                            return_values = self.recursive_identification(by[i:])
                            value = return_values[0]
                            call_function_object.set_path(str(value) + ".")
                            return by[i]
                        elif by[i].name == "LIST_APPEND":
                            i = i + 1
                            return by[i]
                        elif by[i].name == "CALL_METHOD":
                            i = i + 1
                            return ""
                        else:
                            print("CALL_FUNCTION Call Function Reader not registered KW")
                            print(by[i])

                case "LOAD_CONST":
                    call_function_object.add_parameter(str(type(instruction.arg).__name__) + ":" + str(instruction.arg))

            i = i + 1

    # [0] = value, [1] = by updated
    def recursive_identification(self, by):
        counter = 0
        if isinstance(by[counter], Label):
            raw_label = str(by[counter]).removeprefix("<bytecode.instr.Label object at ").removesuffix(">")
            counter = counter + 1
            next_instructions = list()
            while not isinstance(by[counter], Label):
                next_instructions.append(by[counter])
                counter = counter + 1
                if len(by) == counter + 1:
                    break
                if isinstance(by[counter], Label):
                    internal_raw_label = str(by[counter]).removeprefix(
                        "<bytecode.instr.Label object at ").removesuffix(">")
                    if internal_raw_label == raw_label:
                        jump_raw_label = str(by[counter - 1].arg).removeprefix(
                            "<bytecode.instr.Label object at ").removesuffix(">")
                        break
                    next_instructions.append(by[counter])
                    counter = counter + 1
                elif isinstance(by[counter].arg, Label):
                    internal_raw_label = str(by[counter].arg).removeprefix(
                        "<bytecode.instr.Label object at ").removesuffix(">")
                    if internal_raw_label == raw_label:
                        jump_raw_label = str(by[counter - 1].arg).removeprefix(
                            "<bytecode.instr.Label object at ").removesuffix(">")
                        break
                    next_instructions.append(by[counter])
                    counter = counter + 1

            return_values = self.recursive_identification(next_instructions)
            right_value = return_values[0]

            if by[counter].name == "JUMP_IF_TRUE_OR_POP":
                operation_object = OperationObject()
                operation_object.set_operation_type("OR")
                operation_object.set_second_operand(right_value)
                return_values = self.recursive_identification(by[counter:])
                left_value = return_values[0]
                operation_object.set_first_operand(left_value)
                by = return_values[1]
                counter = 0
                return operation_object, by[counter:]
            return right_value, by[counter:]
        elif by[counter].name == "LOAD_CONST":
            value = by[counter].arg
            counter = counter + 1
            return html.escape(str(value)), by[counter:]
        elif by[counter].name == "JUMP_IF_TRUE_OR_POP":
            counter = counter + 1
            return_values = self.recursive_identification(by[counter:])
            value = return_values[0]
            by = return_values[1]
            counter = 0
            return value, by[counter:]
        elif by[counter].name == "LOAD_DEREF":
            value = by[counter].arg
            counter = counter + 1
            return html.escape(str(value)), by[counter:]
        elif by[counter].name == "LOAD_NAME":
            value = by[counter].arg
            counter = counter + 1
            return value, by[counter:]
        elif by[counter].name == "MAKE_FUNCTION":
            # Jumping informations....
            counter = counter + 1
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            function_object = FunctionObject()
            function_object.set_function_name(return_values[0])
            if isinstance(by[counter], Instr):
                internal_bytecode = bytecode.Bytecode.from_code(by[counter].arg)
            else:
                internal_bytecode = bytecode.Bytecode.from_code(by[counter])
            # print(internal_bytecode)
            # return_values = self.recursive_identification(internal_bytecode)
            counter = counter + 1
            return function_object, by[counter:]
        elif by[counter].name == "LOAD_FAST" or by[counter].name == "STORE_FAST":
            value = by[counter].arg
            counter = counter + 1
            variable = VariableObject()
            variable.set_variable_name(value)
            variable.set_type("variable")
            return variable, by[counter:]
        elif by[counter].name == "LOAD_ATTR":
            second_value = by[counter].arg
            counter = counter + 1
            return_values = self.recursive_identification(by[counter:])
            first_value = return_values[0]
            by = return_values[1]
            counter = 0
            return str(first_value) + "." + str(second_value), by[counter:]
        elif by[counter].name == "LOAD_METHOD":
            value = by[counter].arg
            counter = counter + 1
            return value, by[counter:]
        elif by[counter].name == "LOAD_GLOBAL":
            value = by[counter].arg
            counter = counter + 1
            return value, by[counter:]
        elif by[counter].name == "BINARY_ADD":
            counter = counter + 1

            # First Operand
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            add = " + " + str(return_values[0])

            # Second Operand
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            add = str(return_values[0]) + add

            return add, by[counter:]
        elif by[counter].name == "BUILD_LIST":
            number_of_elements = by[counter].arg
            counter = counter + 1
            arguments_counter = 0
            arguments = ""
            while arguments_counter < number_of_elements:
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                arguments = arguments + str(return_values[0]) + ","
                arguments_counter = arguments_counter + 1

            return arguments.removesuffix(","), by[counter:]
        elif by[counter].name == "BUILD_MAP":
            number_of_arguments = by[counter].arg
            counter = counter + 1
            arguments_counter = 0
            list_values = "{"
            while arguments_counter < number_of_arguments:
                # Value
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                value = return_values[0]
                # Key
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                key = return_values[0]
                list_values = list_values + str(key) + ":" + str(value) + ","
                arguments_counter = arguments_counter + 1
            list_values = list_values.removesuffix(",")
            list_values = list_values + "}"
            return list_values, by[counter:]
        elif by[counter].name == "BUILD_TUPLE":
            number_of_arguments = by[counter].arg
            counter = counter + 1
            arguments_counter = 0
            list_values = "("
            while arguments_counter < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                list_values = list_values + str(return_values[0]) + ","
                arguments_counter = arguments_counter + 1

            list_values = list_values.removesuffix(",")
            list_values = list_values + ")"
            return list_values, by[counter:]
        elif by[counter].name == "BINARY_SUBSCR":
            counter = counter + 1
            return_values = self.recursive_identification(by[counter:])
            value_internal = return_values[0]
            by = return_values[1]
            counter = 0
            return_values = self.recursive_identification(by[counter:])
            path = return_values[0]
            by = return_values[1]
            counter = 0
            return str(path) + "[" + str(value_internal) + "]", by[counter:]
        elif by[counter].name == "GET_ITER":
            counter = counter + 1

            # Create a cicle object
            cicle_object = CicleObject()

            # Create a variable for store the condition
            variable_condition = VariableObject()

            if by[counter].name == "CALL_FUNCTION":

                return_values = self.recursive_identification(by[counter:])

                value = return_values[0]
                by = return_values[1]
                counter = 0

                if not isinstance(by[counter], Label):
                    if by[counter].name == "STORE_NAME":
                        counter = counter + 1
                        return "Skip", by[counter:]
                    elif by[counter].name == "LOAD_METHOD":
                        counter = counter + 1
                        return "Skip", by[counter:]
                    elif by[counter].name == "CALL_FUNCTION":
                        counter = counter + 1
                        return "Skip", by[counter:]

                variable_condition.set_argument(value)
                variable_condition.set_type("CallFunction")
            elif by[counter].name == "LOAD_CONST" or by[counter].name == "LOAD_FAST" \
                    or by[counter].name == "CALL_METHOD" or by[counter].name == "LOAD_ATTR" \
                    or by[counter].name == "LOAD_NAME" or by[counter].name == "BINARY_SUBSCR" \
                    or by[counter].name == "LOAD_DEREF" or by[counter].name == "BINARY_SUBTRACT" \
                    or by[counter].name == "CALL_FUNCTION_EX":
                return_values = self.recursive_identification(by[counter:])
                variable_condition.set_argument(return_values[0])
                variable_condition.set_type(str(type(return_values[0]).__name__))
                by = return_values[1]
                counter = 0
            else:
                print("GET_ITER Not registered")
                print(by[counter])

            return_values = self.recursive_identification(by[counter:])
            value = return_values[0]
            by = return_values[1]
            counter = 0
            if not isinstance(value, (FunctionObject, CallFunctionObject, OperationObject)):
                if value.__contains__("<"):
                    value = value.removeprefix("<")
                    value = value.removesuffix(">")
                variable_condition.set_type(str(type(value).__name__))
                variable_condition.set_variable_name(value)
            cicle_object.set_condition(variable_condition)
            return cicle_object, by[counter:]
        elif by[counter].name == "CALL_METHOD":
            number_of_arguments = by[counter].arg
            counter_arguments = 0
            counter = counter + 1

            # Create a call function Object
            call_function = CallFunctionObject()

            # Parameters
            while counter_arguments < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                call_function.add_parameter(return_values[0])
                by = return_values[1]
                counter = 0
                counter_arguments = counter_arguments + 1

            # Name of method
            if by[counter].name == "LOAD_METHOD":
                return_values = self.recursive_identification(by[counter:])
                call_function.set_method_name("." + return_values[0])
                by = return_values[1]
                counter = 0

            # Path of method
            return_values = self.recursive_identification(by[counter:])
            path = call_function.path
            if path == "":
                path = str(return_values[0])
            else:
                if path.endswith("."):
                    path = path + str(return_values[0])
                else:
                    path = path + "." + str(return_values[0])
            call_function.set_path(path)
            by = return_values[1]
            counter = 0
            return call_function, by[counter:]
        elif by[counter].name == "CALL_FUNCTION":
            number_of_arguments = by[counter].arg
            counter_arguments = 0
            counter = counter + 1

            # Create a call function Object
            call_function = CallFunctionObject()

            # Parameters
            while counter_arguments < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                call_function.add_parameter(return_values[0])
                by = return_values[1]
                counter = 0
                counter_arguments = counter_arguments + 1

            return_values = self.recursive_identification(by[counter:])
            call_function.set_method_name(return_values[0])
            by = return_values[1]
            counter = 0
            return call_function, by[counter:]
        elif by[counter].name == "CALL_FUNCTION_KW":
            number_of_arguments = by[counter].arg
            counter_arguments = 0
            counter = counter + 1

            list_arguments = by[counter].arg
            counter = counter + 1

            # Create a call function Object
            call_function = CallFunctionObject()

            # Parameters
            while counter_arguments < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                parameter = return_values[0]
                if parameter is None:
                    parameter = "None"
                try:
                    parameter = list_arguments[counter_arguments] + " = " + str(parameter)
                except IndexError:
                    parameter = str(return_values[0])
                call_function.add_parameter(parameter)
                by = return_values[1]
                counter = 0
                counter_arguments = counter_arguments + 1

            return_values = self.recursive_identification(by[counter:])
            call_function.set_method_name(return_values[0])
            by = return_values[1]
            counter = 0
            return call_function, by[counter:]
        elif by[counter].name == "BINARY_MODULO":
            counter = counter + 1
            # First Part
            return_values = self.recursive_identification(by[counter:])
            module = return_values[0]
            by = return_values[1]
            counter = 0
            module = " % " + str(module)
            # Second Part
            return_values = self.recursive_identification(by[counter:])
            module = str(return_values[0]) + module
            by = return_values[1]
            counter = 0
            return module, by[counter:]
        elif by[counter].name == "BINARY_SUBTRACT":
            counter = counter + 1

            # First Operand
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            subtract = " - " + str(return_values[0])

            # Second Operand
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            subtract = str(return_values[0]) + subtract

            return subtract, by[counter:]
        elif by[counter].name == "BINARY_MULTIPLY":
            counter = counter + 1

            # First Operand
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            subtract = " * " + str(return_values[0])

            # Second Operand
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            subtract = str(return_values[0]) + subtract

            return subtract, by[counter:]
        elif by[counter].name == "BINARY_TRUE_DIVIDE":
            counter = counter + 1

            # First Operand
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            subtract = " / " + str(return_values[0])

            # Second Operand
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            subtract = str(return_values[0]) + subtract

            return subtract, by[counter:]
        elif by[counter].name == "BUILD_CONST_KEY_MAP":
            number_of_arguments = by[counter].arg
            counter = counter + 1
            return_values = self.recursive_identification(by[counter:])
            arguments_list = return_values[0]
            by = return_values[1]
            counter = 0
            counter_arguments = 0
            raw_map = "{"
            while counter_arguments < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                raw_map = raw_map + arguments_list[counter_arguments] + ":" + str(return_values[0]) + ","
                by = return_values[1]
                counter = 0
                counter_arguments = counter_arguments + 1
            raw_map = raw_map.removesuffix(",") + "}"
            return raw_map, by[counter:]
        elif by[counter].name == "BINARY_AND":
            counter = counter + 1
            operation_object = OperationObject()
            operation_object.set_operation_type("AND")
            # Left Operand
            return_values = self.recursive_identification(by[counter:])
            operation_object.set_first_operand(return_values[0])
            by = return_values[1]
            counter = 0
            # Right Operand
            return_values = self.recursive_identification(by[counter:])
            operation_object.set_second_operand(return_values[0])
            by = return_values[1]
            counter = 0
            return operation_object, by[counter:]
        elif by[counter].name == "BINARY_OR":
            counter = counter + 1
            operation_object = OperationObject()
            operation_object.set_operation_type("OR")
            # Left Operand
            return_values = self.recursive_identification(by[counter:])
            operation_object.set_first_operand(return_values[0])
            by = return_values[1]
            counter = 0
            # Right Operand
            return_values = self.recursive_identification(by[counter:])
            operation_object.set_second_operand(return_values[0])
            by = return_values[1]
            counter = 0
            return operation_object, by[counter:]
        elif by[counter].name == "BINARY_POWER":
            counter = counter + 1

            # First Operand
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            subtract = " ** " + str(return_values[0])

            # Second Operand
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            subtract = str(return_values[0]) + subtract
            return subtract, by[counter:]
        elif by[counter].name.__contains__("_OP"):
            operation_name = str(by[counter].arg)
            if not operation_name.__contains__("."):
                operation_name = by[counter].name.removesuffix("_OP").lower().capitalize()
            operation_object = OperationObject()
            operation_object.set_operation_type(operation_name)
            counter = counter + 1
            # First Operand
            return_values = self.recursive_identification(by[counter:])
            operation_object.set_first_operand(return_values[0])
            by = return_values[1]
            counter = 0
            # Second Operand
            return_values = self.recursive_identification(by[counter:])
            operation_object.set_second_operand(return_values[0])
            by = return_values[1]
            counter = 0
            return operation_object, by[counter:]
        elif by[counter].name == "LOAD_CLOSURE":
            value = by[counter].arg
            counter = counter + 1
            return value, by[counter:]
        elif by[counter].name == "LIST_EXTEND":
            number_of_arguments = by[counter].arg
            counter = counter + 1
            counter_arguments = 0
            arguments = "["
            while counter_arguments < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                arguments = arguments + str(return_values[0]) + ","
                counter_arguments = counter_arguments + 1

            arguments = arguments.removesuffix(",")
            arguments = arguments + "]"

            # This is for jump BUILD_LIST
            counter = counter + 1

            return arguments, by[counter:]
        elif by[counter].name == "BUILD_SLICE":
            number_of_arguments = by[counter].arg
            counter = counter + 1
            arguments_counter = 0
            raw_slice = list()
            # Arguments
            while arguments_counter < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                raw_slice.append(return_values[0])
                arguments_counter = arguments_counter + 1

            raw_slice.reverse()
            final_slice = ""
            while len(raw_slice) != 0:
                final_slice = final_slice + str(raw_slice[0]) + ":"
                raw_slice.remove(raw_slice[0])
            final_slice = final_slice.removesuffix(":")

            return final_slice, by[counter:]
        elif by[counter].name == "LIST_APPEND":
            number_of_arguments = by[counter].arg
            counter = counter + 1
            arguments_counter = 0
            arguments = ""
            while arguments_counter < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                arguments = arguments + str(return_values[0]) + ","
                arguments_counter = arguments_counter + 1

            arguments = arguments.removesuffix(",")
            return arguments, by[counter:]
        elif by[counter].name == "BUILD_STRING":
            number_of_arguments = by[counter].arg
            counter = counter + 1
            arguments_counter = 0
            arguments = ""
            while arguments_counter < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                arguments = arguments + str(return_values[0]) + ","
                arguments_counter = arguments_counter + 1

            arguments = arguments.removesuffix(",")
            return arguments, by[counter:]
        elif by[counter].name == "FORMAT_VALUE":
            number_of_arguments = by[counter].arg
            counter = counter + 1
            arguments_counter = 0
            arguments = ""
            while arguments_counter < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                arguments = arguments + str(return_values[0]) + ","
                arguments_counter = arguments_counter + 1

            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0

            arguments = arguments.removesuffix(",")
            return return_values[0], by[counter:]
        elif by[counter].name == "UNARY_NEGATIVE":
            operation_name = "Unary Negative"
            operation_object = OperationObject()
            operation_object.set_operation_type(operation_name)
            counter = counter + 1
            # Operand
            return_values = self.recursive_identification(by[counter:])
            operation_object.set_second_operand(return_values[0])
            by = return_values[1]
            counter = 0
            return operation_object, by[counter:]
        elif by[counter].name == "CALL_FUNCTION_EX":
            number_of_arguments = by[counter].arg
            counter_arguments = 0
            counter = counter + 1

            # Create a call function Object
            call_function = CallFunctionObject()

            # Parameters
            while counter_arguments < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                call_function.add_parameter(return_values[0])
                by = return_values[1]
                counter = 0
                counter_arguments = counter_arguments + 1

            return_values = self.recursive_identification(by[counter:])
            call_function.set_method_name(return_values[0])
            by = return_values[1]
            counter = 0
            return call_function, by[counter:]
        elif by[counter].name == "DICT_MERGE":
            operation_object = OperationObject()
            operation_object.set_operation_type("Merge")
            number_of_arguments = by[counter].arg
            arguments_counter = 0
            counter = counter + 1

            arguments = ""
            while arguments_counter < number_of_arguments:
                # First Part
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                arguments = arguments + str(return_values[0]) + ","
                arguments_counter = arguments_counter + 1

            arguments = arguments.removesuffix(",")
            operation_object.set_second_operand(arguments)

            # Second Part
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            operation_object.set_first_operand(return_values[0])

            return operation_object, by[counter:]
        elif by[counter].name == "BINARY_FLOOR_DIVIDE":
            counter = counter + 1
            operation_object = OperationObject()
            operation_object.set_operation_type("FLOOR DIVIDE")
            # Left Operand
            return_values = self.recursive_identification(by[counter:])
            operation_object.set_first_operand(return_values[0])
            by = return_values[1]
            counter = 0
            # Right Operand
            return_values = self.recursive_identification(by[counter:])
            operation_object.set_second_operand(return_values[0])
            by = return_values[1]
            counter = 0
            return operation_object, by[counter:]
        elif by[counter].name == "UNARY_INVERT":
            counter = counter + 1
            operation_object = OperationObject()
            operation_object.set_operation_type("UNARY INVERT")

            # Operand
            return_values = self.recursive_identification(by[counter:])
            operation_object.set_first_operand(return_values[0])
            by = return_values[1]
            counter = 0
            return operation_object, by[counter:]
        elif by[counter].name == "UNARY_NOT":
            counter = counter + 1
            operation_object = OperationObject()
            operation_object.set_operation_type("UNARY NOT")

            # Operand
            return_values = self.recursive_identification(by[counter:])
            operation_object.set_first_operand(return_values[0])
            by = return_values[1]
            counter = 0
            return operation_object, by[counter:]
        elif by[counter].name == "SET_UPDATE":
            counter = counter + 1

            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0

            return return_values[0], by[counter:]
        elif by[counter].name == "BUILD_SET":
            number_of_arguments = by[counter].arg
            counter = counter + 1
            arguments_counter = 0
            list_values = "("
            while arguments_counter < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                list_values = list_values + str(return_values[0]) + ","
                arguments_counter = arguments_counter + 1

            list_values = list_values.removesuffix(",")
            list_values = list_values + ")"
            return list_values, by[counter:]
        elif by[counter].name == "MAP_ADD":
            number_of_arguments = by[counter].arg
            arguments_counter = 0
            counter = counter + 1

            arguments = ""
            while arguments_counter < number_of_arguments:
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                arguments = arguments + str(return_values[0]) + ","
                arguments_counter = arguments_counter + 1

            return arguments, by[counter:]
        elif by[counter].name == "LIST_TO_TUPLE":

            new_tuple = "("

            counter = counter + 1
            # First Part
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            new_tuple = new_tuple + return_values[0] + ","

            # Second Part
            return_values = self.recursive_identification(by[counter:])
            by = return_values[1]
            counter = 0
            new_tuple = new_tuple + str(return_values[0]) + ")"

            return new_tuple, by[counter:]
        else:
            print("Recursive identification not registered Call Function Reader")
            print(by[counter])
            exit(-1)
