from bytecode import Label
from bytecode import bytecode
from Objects.CallFunctionObject import CallFunctionObject
from Objects.CicleObject import CicleObject
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
                    count = 0
                    # Parameters
                    while count < number_of_args:
                        if by[i + 1].name == "LOAD_CONST":
                            self.read_call_function(call_function_object, [by[i + 1]], debug_active)
                            count = count + 1
                            i = i + 1
                            continue
                        elif by[i + 1].name == "LOAD_NAME":
                            call_function_object.add_parameter(by[i + 1].arg)
                            count = count + 1
                            i = i + 1
                            continue
                        elif by[i + 1].name == "LOAD_FAST":
                            call_function_object.add_parameter(by[i + 1].arg)
                            count = count + 1
                            i = i + 1
                            continue
                        elif by[i + 1].name == "CALL_METHOD":
                            internal_call_function = CallFunctionObject()
                            fun_name = self.read_call_function(internal_call_function, by[i + 1:len(by)], debug_active)
                            if isinstance(fun_name, list):
                                by = fun_name
                            else:
                                by = [fun_name, fun_name]
                            call_function_object.add_parameter(internal_call_function)
                            count = count + 1
                            continue
                        # BodyFunction -> BINARY_SUBSCR
                        elif by[i + 1].name == "BINARY_SUBSCR":
                            call_function_object.add_parameter("[" + str(by[i + 2].arg) + "]")
                            count = count + 1
                            i = i + 2
                        # BodyFunction -> BINARY_ADD
                        elif by[i + 1].name == "BINARY_ADD":
                            call_function_object.add_parameter("[" + str(by[i + 2].arg) + "]")
                            count = count + 1
                            i = i + 2
                        elif by[i + 1].name == "LOAD_GLOBAL":
                            call_function_object.add_parameter(by[i + 1].arg)
                            count = count + 1
                            i = i + 1
                        else:
                            print("ERROR PARAMETERS")
                            print(by[i + 1])
                    if by[i + 1].name == "LOAD_METHOD":
                        call_function_object.set_method_name("." + by[i + 1].arg)
                        i = i + 1
                    if by[i + 1].name == "LOAD_NAME":
                        path = call_function_object.path
                        if path == "":
                            path = by[i + 1].arg
                        else:
                            if path.endswith("."):
                                path = path + by[i + 1].arg
                            else:
                                path = path + "." + by[i + 1].arg
                        call_function_object.set_path(path)
                        i = i + 1
                        return by[i:len(by)]
                    if by[i + 1].name == "LOAD_FAST":
                        path = call_function_object.path
                        if path == "":
                            path = by[i + 1].arg
                        else:
                            if path.endswith("."):
                                path = path + by[i + 1].arg
                            else:
                                path = path + "." + by[i + 1].arg
                        call_function_object.set_path(path)
                        i = i + 1
                        return by[i:len(by)]
                    # CallMethod -> CallMethod.CallMethod
                    elif by[i + 1].name == "CALL_METHOD":
                        internal_call_method = CallFunctionObject()
                        fun_name = self.read_call_function(internal_call_method, by[i + 1:len(by)], debug_active)
                        call_function_object.add_concat(internal_call_method)
                        return fun_name
                    # CallMethod -> LOAD_NAME LOAD_ATTR LOAD_METHOD CALL_METHOD
                    elif by[i + 1].name == "LOAD_ATTR":
                        path = call_function_object.path
                        if path == "":
                            path = by[i + 1].arg
                        else:
                            if path.endswith("."):
                                path = path + by[i + 1].arg
                            else:
                                path = path + "." + by[i + 1].arg
                        call_function_object.set_path(path)
                        i = i + 1
                        if by[i + 1].name == "LOAD_NAME":
                            path = call_function_object.path
                            if path == "":
                                path = by[i + 1].arg
                            else:
                                if path.endswith("."):
                                    path = by[i + 1].arg + path
                                else:
                                    path = by[i + 1].arg + "." + path
                            call_function_object.set_path(path)
                            i = i + 1
                            # If is a call function there is a return
                            # If is a call method there isn't a return
                            try:
                                return by[i + 1]
                            except:
                                pass
                        elif by[i + 1].name == "LOAD_FAST":
                            path = call_function_object.path
                            if path == "":
                                path = by[i + 1].arg
                            else:
                                if path.endswith("."):
                                    path = by[i + 1].arg + path
                                else:
                                    path = by[i + 1].arg + "." + path
                            call_function_object.set_path(path)
                            i = i + 1
                            # If is a call function there is a return
                            # If is a call method there isn't a return
                            try:
                                return by[i + 1]
                            except:
                                pass
                    # CallMethod -> CallMethod.CallFunction
                    elif by[i + 1].name == "CALL_FUNCTION":
                        internal_call_method = CallFunctionObject()
                        fun_name = self.read_call_function(internal_call_method, by[i + 1:len(by)], debug_active)
                        call_function_object.add_concat(internal_call_method)
                        return fun_name
                    # CallMethod -> LOAD_GLOBAL LOAD_ATTR LOAD_METHOD CALL_METHOD
                    elif by[i+1].name == "LOAD_GLOBAL":
                        path = call_function_object.path
                        if path == "":
                            path = by[i + 1].arg
                        else:
                            if path.endswith("."):
                                path = path + by[i + 1].arg
                            else:
                                path = path + "." + by[i + 1].arg
                        call_function_object.set_path(path)
                        i = i + 1
                        return by[i:len(by)]
                    elif by[i + 1].name == "BINARY_SUBSCR":
                        path = call_function_object.path
                        if path == "":
                            path = by[i + 3].arg + "[" + by[i + 2].arg + "]"
                        else:
                            if path.endswith("."):
                                path = path + by[i + 3].arg + "[" + by[i + 2].arg + "]"
                            else:
                                path = path + "." + by[i + 3].arg + "[" + by[i + 2].arg + "]"
                        call_function_object.set_path(path)
                        i = i + 2
                        return by[i:len(by)]
                    else:
                        print("ERROR CALL_METHOD")
                        print(by[i + 1])

                # CallFunction -> LOAD_NAME BodyFunction CALL_FUNCTION
                case "CALL_FUNCTION":
                    number_of_args = instruction.arg
                    count = 0
                    # Body Function
                    while count < number_of_args:
                        # BodyFunction -> LOAD_CONST
                        if by[i + 1].name == "LOAD_CONST":
                            self.read_call_function(call_function_object, [by[i + 1]], debug_active)
                            count = count + 1
                            i = i + 1
                            continue
                        # BodyFunction -> LOAD_NAME
                        elif by[i + 1].name == "LOAD_NAME":
                            call_function_object.add_parameter(by[i + 1].arg)
                            count = count + 1
                            i = i + 1
                            continue
                        # BodyFunction -> LOAD_FAST
                        elif by[i + 1].name == "LOAD_FAST":
                            call_function_object.add_parameter(by[i + 1].arg)
                            count = count + 1
                            i = i + 1
                        # BodyFunction -> CallMethod
                        elif by[i + 1].name == "CALL_METHOD":
                            internal_call_function = CallFunctionObject()
                            fun_name = self.read_call_function(internal_call_function, by[i + 1:len(by)], debug_active)
                            if isinstance(fun_name, list):
                                by = fun_name
                            else:
                                by = [fun_name, fun_name]
                            call_function_object.add_parameter(internal_call_function)
                            call_function_object.set_method_name(fun_name)
                            count = count + 1
                            continue
                        # BodyFunction -> CallFunction
                        elif by[i + 1].name == "CALL_FUNCTION":
                            internal_call_function = CallFunctionObject()
                            fun_name = self.read_call_function(internal_call_function, by[i + 1:len(by)], debug_active)
                            if isinstance(fun_name, list):
                                by = fun_name
                            else:
                                by = [fun_name, fun_name]
                            call_function_object.add_parameter(internal_call_function)
                            call_function_object.set_method_name(fun_name.arg)
                            count = count + 1
                            continue
                        # BodyFunction -> Cicle
                        elif by[i + 1].name == "GET_ITER":

                            i = i + 1

                            next_instructions = [by[i + 1]]

                            # Create a cicle object
                            cicle_object = CicleObject()

                            # Create a variable for store the condition
                            variable_condition = VariableObject()

                            if next_instructions[0].name == "CALL_FUNCTION":
                                next_instructions = list()
                                i = i + 1
                                while by[i].name != "POP_TOP" and by[i].name != "MAKE_FUNCTION" and by[
                                    i].name != "NOP" and by[i].name != "STORE_NAME" and by[
                                    i].name != "LOAD_BUILD_CLASS" and by[i].name != "RETURN_VALUE":
                                    next_instructions.append(by[i])
                                    i = i + 1

                                if not isinstance(by[i + 1], Label):
                                    if by[i + 1].name == "STORE_NAME":
                                        i = i + 1
                                        continue
                                    elif by[i + 1].name == "LOAD_METHOD":
                                        i = i + 1
                                        continue
                                    elif by[i + 1].name == "CALL_FUNCTION":
                                        i = i + 1
                                        continue

                                # Create a call function object for condtion
                                call_function = CallFunctionObject()

                                self.read_call_function(call_function, next_instructions, debug_active)

                                variable_condition.set_argument(call_function)
                                variable_condition.set_type("CallFunction")
                            elif next_instructions[0].name == "LOAD_CONST":
                                variable_condition.set_argument(next_instructions[0].arg)
                                variable_condition.set_type(str(type(next_instructions[0].arg).__name__))

                            if by[i + 1].arg.__contains__("<"):
                                temp = by[i + 1].arg.removeprefix("<")
                                temp = temp.removesuffix(">")
                                by[i + 1].arg = temp
                            variable_condition.set_type(by[i + 1].arg)
                            variable_condition.set_variable_name(by[i + 1].arg)
                            cicle_object.set_condition(variable_condition)

                            # Add cicle at instructions of File Object
                            call_function_object.add_parameter(cicle_object)
                            count = count + 1
                            continue
                        # BodyFunction -> BINARY_SUBSCR
                        elif by[i + 1].name == "BINARY_SUBSCR":
                            call_function_object.add_parameter("[" + str(by[i + 2].arg) + "]")
                            count = count + 1
                            i = i + 2
                        # BodyFunction -> BINARY_ADD
                        elif by[i + 1].name == "BINARY_ADD":
                            call_function_object.add_parameter("[" + str(by[i + 2].arg) + "]")
                            count = count + 1
                            i = i + 2
                        elif by[i + 1].name == "LOAD_ATTR":
                            variable_name = by[i + 2].arg + "." + by[i + 1].arg
                            call_function_object.add_parameter(variable_name)
                            count = count + 1
                            i = i + 2
                        elif by[i + 1].name == "LOAD_GLOBAL":
                            call_function_object.add_parameter(by[i + 1].arg)
                            count = count + 1
                            i = i + 1
                        else:
                            print("ERROR CALL_FUNCTION PARAMETERS")
                            print(count)
                            print(by[i + 1])

                    try:
                        if by[i + 1].name == "LOAD_NAME":
                            call_function_object.set_method_name(by[i + 1].arg)
                            i = i + 1
                            return by[i + 1]
                        elif by[i + 1].name == "LOAD_GLOBAL":
                            call_function_object.set_method_name(by[i + 1].arg)
                            i = i + 1
                            return by[i + 1]
                        elif by[i + 1].name == "LOAD_CONST":
                            call_function_object.set_method_name(by[i + 1].arg)
                            i = i + 1
                            if by[i].arg.__contains__("<"):
                                temp = by[i].arg.removeprefix("<")
                                temp = temp.removesuffix(">")
                                by[i].arg = temp
                            return by[i + 1]
                        elif by[i + 1].name == "LOAD_FAST":
                            call_function_object.set_method_name(by[i + 1].arg)
                            i = i + 1
                            return by[i + 1]
                        else:
                            print("CALL_FUNCTION Call Function Reader not registered")
                            print(by[i + 1])
                    except:
                        pass

                case "LOAD_CONST":
                    call_function_object.add_parameter(str(type(instruction.arg).__name__) + ":" + str(instruction.arg))

            i = i + 1
