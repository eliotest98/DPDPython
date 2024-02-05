from Objects.CallFunctionObject import CallFunctionObject


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
                            call_function_object.add_parameter(by[i + 1].name)
                            count = count + 1
                            i = i + 1
                            continue
                        elif by[i + 1].name == "LOAD_FAST":
                            call_function_object.add_parameter(by[i + 1].name)
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
                        else:
                            print("ERROR CALL_FUNCTION")
                            print(count)
                            print(by[i + 1])

                    try:
                        if by[i + 1].name == "LOAD_NAME":
                            call_function_object.set_method_name(by[i + 1].arg)
                            i = i + 1
                            return by[i + 1]

                        if by[i + 1].name == "LOAD_GLOBAL":
                            call_function_object.set_method_name(by[i + 1].arg)
                            i = i + 1
                            return by[i + 1]
                    except:
                        pass

                case "LOAD_CONST":
                    call_function_object.add_parameter(instruction.arg)

            i = i + 1
