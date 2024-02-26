from bytecode import Label

from Objects.CallFunctionObject import CallFunctionObject
from Objects.ImportObject import ImportObject
from Objects.ReturnObject import ReturnObject
from Objects.VariableObject import VariableObject
from Readers.CallFunctionReader import CallFunctionReader


class FunctionReader:

    def read_function(self, function_object, bytecode_instructions, debug_active):
        if debug_active == 1:
            print("\n" + function_object.function_name + " Function Reading...")

        # Copy for delete instructions when visited
        by = bytecode_instructions

        # Instruction Counter
        i = 0

        # List the instructions
        while i < len(by):
            instruction = by[i]
            if isinstance(instruction, Label):
                i = i + 1
                continue
            if debug_active == 1:
                print(instruction)
            match instruction.name:

                case "RETURN_VALUE":
                    previous_instructions = [by[i - 1]]

                    # ReturnValue -> LOAD_CONST RETURN_VALUE
                    if previous_instructions[0].name == "LOAD_CONST":
                        return_object = ReturnObject()
                        return_object.set_type(str(type(previous_instructions[0].arg).__name__))
                        return_object.set_argument(previous_instructions[0].arg)
                        function_object.set_return_object(return_object)
                    # ReturnValue -> LOAD_FAST RETURN_VALUE
                    elif previous_instructions[0].name == "LOAD_FAST":
                        # Create a Variable Object
                        variable = VariableObject()
                        variable.set_variable_name(previous_instructions[0].arg)
                        return_object = ReturnObject()
                        return_object.set_type("variable")
                        return_object.set_argument(variable)
                        # Set the return value
                        function_object.set_return_object(return_object)
                    # ReturnValue -> CALL_METHOD RETURN_VALUE
                    elif previous_instructions[0].name == "CALL_METHOD":
                        previous_instruction = list()
                        count = i - 1
                        try:
                            while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[
                                count].name != "STORE_NAME" and by[count].name != "STORE_FAST" and by[
                                count].name != "LOAD_FAST":
                                previous_instruction.append(by[count])
                                count = count - 1

                            previous_instruction.append(by[count])

                            try:
                                if by[i + 1].name == "CALL_FUNCTION":
                                    i = i + 1
                                    continue
                                elif by[i + 1].name == "LOAD_METHOD":
                                    i = i + 1
                                    continue
                            except:
                                pass

                        except:
                            pass

                        # Create a call function object
                        call_function = CallFunctionObject()

                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                        return_object = ReturnObject()
                        return_object.set_argument(call_function)
                        return_object.set_type("CallMethod")
                        # Add the variable at instructions of file object
                        function_object.set_return_object(return_object)
                    else:
                        print("Not registered")
                        print(instruction)
                        print(previous_instructions[0])

                # CallMethod -> LOAD_FAST LOAD_ATTR LOAD_METHOD CALL_METHOD
                case "CALL_METHOD":
                    previous_instruction = list()
                    count = i - 1
                    previous_instruction.append(instruction)
                    try:
                        while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[count].name != "STORE_NAME" \
                                and by[count].name != "STORE_FAST":
                            previous_instruction.append(by[count])
                            count = count - 1
                    except:
                        print("")

                    if by[i + 1].name == "CALL_METHOD":
                        i = i + 1
                        continue
                    if by[i + 1].name == "CALL_FUNCTION":
                        i = i + 1
                        continue
                    elif by[i + 1].name == "LOAD_METHOD":
                        i = i + 1
                        continue
                    elif by[i + 1].name == "STORE_NAME":
                        i = i + 1
                        continue
                    elif by[i + 1].name == "LOAD_CONST":
                        i = i + 1
                        continue
                    elif by[i + 1].name == "RETURN_VALUE":
                        i = i + 1
                        continue
                    elif by[i + 1].name == "STORE_FAST":
                        i = i + 1
                        continue

                    # Create a call function object
                    call_function = CallFunctionObject()

                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                    # Add the call function at instructions of file object
                    function_object.add_instruction(call_function)

                # CallFunction -> LOAD_GLOBAL Some informations CALL_FUNCTION
                case "CALL_FUNCTION":
                    previous_instruction = list()
                    count = i - 1
                    previous_instruction.append(instruction)
                    while by[count].name != "LOAD_GLOBAL":
                        previous_instruction.append(by[count])
                        count = count - 1
                    previous_instruction.append(by[count])

                    if by[i + 1].name == "STORE_FAST":
                        i = i + 1
                        continue

                    if by[i + 1].name == "LOAD_FAST":
                        i = i + 1
                        continue

                    if by[i + 1].name == "LOAD_METHOD":
                        i = i + 1
                        continue

                    # Create a call function object
                    call_function = CallFunctionObject()

                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                    # Add the call function at instructions of function object
                    function_object.add_instruction(call_function)

                case "STORE_ATTR":
                    previous_instructions = [by[i - 1]]
                    # Variable(Function) -> LOAD_CONST LOAD_FAST STORE_ATTR
                    if previous_instructions[0].name == "LOAD_FAST":
                        previous_instructions.append(by[i - 2])
                        # Variable -> LOAD_CONST STORE_FAST STORE_ATTR
                        if previous_instructions[1].name == "LOAD_CONST":
                            # Create a variable object
                            variable = VariableObject()
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                            variable.set_argument(previous_instructions[1].arg)
                            variable.set_type(str(type(previous_instructions[1].arg).__name__))
                            # Add variabile at variable list of class
                            function_object.add_variable(variable)
                        # Variable -> LOAD_FAST STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "LOAD_FAST":
                            # Create the Variable Object
                            other_variable = VariableObject()
                            other_variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                            # Create the 2* Variable Object
                            variable = VariableObject()
                            variable.set_variable_name(previous_instructions[1].arg)
                            # Set the 1* Variable Object at 2* Variable Object
                            other_variable.set_argument(variable)
                            other_variable.set_type("variable")
                            # Add the variable at instructions
                            function_object.add_instruction(other_variable)
                        # Variable -> BUILD_LIST LOAD_CONST LIST_EXTEND STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "LIST_EXTEND":
                            previous_instructions.append(by[i - 3])
                            previous_instructions.append(by[i - 4])
                            previous_instructions.reverse()
                            # Create a variable object
                            variable = VariableObject()
                            # The current instruction contains the name of variable
                            variable.set_variable_name(previous_instructions[3].arg + "." + instruction.arg)
                            variable.set_argument(previous_instructions[1].arg)
                            variable.set_type(str(type(previous_instructions[1].arg).__name__))
                            # Add the variable at variables list:
                            function_object.add_variable(variable)
                        # Variable -> LOAD_CONST LOAD_CONST BUILD_MAP STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "BUILD_MAP":
                            previous_instructions.append(by[i - 3])
                            previous_instructions.append(by[i - 4])
                            previous_instructions.reverse()
                            # Create a variable object
                            variable = VariableObject()
                            # The current instruction contains the name of variable
                            variable.set_variable_name(previous_instructions[3].arg + "." + instruction.arg)
                            variable.set_argument(previous_instructions[0].arg + ":" + previous_instructions[1].arg)
                            variable.set_type("dictionary")
                            # Add the variable at variables list:
                            function_object.add_variable(variable)
                        # Variable -> BUILD_SET LOAD_CONST SET_UPDATE STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "SET_UPDATE":
                            previous_instructions.append(by[i - 3])
                            previous_instructions.append(by[i - 4])
                            previous_instructions.reverse()
                            # Create a variable object
                            variable = VariableObject()
                            # The current instruction contains the name of variable
                            variable.set_variable_name(previous_instructions[3].arg + "." + instruction.arg)
                            variable.set_argument(previous_instructions[1].arg)
                            variable.set_type(str(type(previous_instructions[1].arg).__name__))
                            # Add the variable at variables list:
                            function_object.add_variable(variable)
                        # Variable -> CallMethod STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "CALL_METHOD":
                            previous_instruction = list()
                            count = i - 1
                            previous_instruction.append(instruction)
                            while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[
                                count].name != "STORE_FAST":
                                previous_instruction.append(by[count])
                                count = count - 1

                            self_value = previous_instructions[0]

                            if by[i + 1].name == "CALL_FUNCTION":
                                i = i + 1
                                continue
                            elif by[i + 1].name == "LOAD_METHOD":
                                i = i + 1
                                continue

                            # Create a call function object
                            call_function = CallFunctionObject()

                            call_function_reader = CallFunctionReader()
                            call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                            # Create a variable object
                            variable = VariableObject()

                            variable.set_variable_name(self_value.arg + "." + instruction.arg)
                            variable.set_argument(call_function)
                            variable.set_type("CallMethod")

                            # Add the variable at instructions of file object
                            function_object.add_instruction(variable)
                        # Variable -> CallFunction STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "CALL_FUNCTION":
                            previous_instructions.append(by[i - 2])
                            previous_instructions.append(by[i - 3])
                            previous_instructions.append(by[i - 4])
                            previous_instructions.append(by[i - 5])
                            previous_instructions.append(by[i - 6])
                            previous_instructions.reverse()
                            if isinstance(previous_instructions[1].arg, str):
                                previous_instruction = list()
                                count = i - 1
                                previous_instruction.append(instruction)
                                while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[
                                    count].name != "STORE_FAST" and by[count].name != "STORE_ATTR":
                                    previous_instruction.append(by[count])
                                    count = count - 1

                                # Create a call function object
                                call_function = CallFunctionObject()

                                call_function_reader = CallFunctionReader()
                                call_function_reader.read_call_function(call_function, previous_instruction,
                                                                        debug_active)

                                # Create a variable object
                                variable = VariableObject()
                                variable.set_variable_name(
                                    previous_instruction[1].arg + "." + previous_instruction[0].arg)
                                variable.set_argument(call_function)
                                variable.set_type("CallFunction")

                                # Add the call function at instructions of file object
                                function_object.add_instruction(variable)

                                i = i + 1
                                continue
                        else:
                            print("Not registered")
                            print(instruction)
                            print(previous_instructions[0])
                            print(previous_instructions[1])
                    else:
                        print("Not registered")
                        print(instruction)
                        print(previous_instructions[0])

                case "STORE_FAST":
                    previous_instructions = [by[i - 1]]
                    # Variable -> LOAD_CONST STORE_FAST
                    if previous_instructions[0].name == "LOAD_CONST":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(previous_instructions[0].arg)
                        variable.set_type(str(type(previous_instructions[0].arg).__name__))
                        # Add variabile at variable list of class
                        function_object.add_variable(variable)
                    # Variable -> LOAD_FAST STORE_FAST
                    elif previous_instructions[0].name == "LOAD_FAST":
                        # Create the Variable Object
                        other_variable = VariableObject()
                        other_variable.set_variable_name(previous_instructions[0].arg)
                        # Create the 2* Variable Object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        # Set the 1* Variable Object at 2* Variable Object
                        variable.set_argument(other_variable)
                        variable.set_type("variable")
                        # Add the variable at instructions
                        function_object.add_instruction(variable)
                    # Variable -> BUILD_LIST LOAD_CONST LIST_EXTEND STORE_FAST
                    elif previous_instructions[0].name == "LIST_EXTEND":
                        previous_instructions.append(by[i - 2])
                        previous_instructions.append(by[i - 3])
                        previous_instructions.reverse()
                        # Create a variable object
                        variable = VariableObject()
                        # The current instruction contains the name of variable
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(previous_instructions[1].arg)
                        variable.set_type(str(type(previous_instructions[1].arg).__name__))
                        # Add the variable at variables list:
                        function_object.add_variable(variable)
                    # Variable -> LOAD_CONST LOAD_CONST BUILD_MAP STORE_FAST
                    elif previous_instructions[0].name == "BUILD_MAP":
                        previous_instructions.append(by[i - 2])
                        previous_instructions.append(by[i - 3])
                        previous_instructions.reverse()
                        # Create a variable object
                        variable = VariableObject()
                        # The current instruction contains the name of variable
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(previous_instructions[0].arg + ":" + previous_instructions[1].arg)
                        variable.set_type("dictionary")
                        # Add the variable at variables list:
                        function_object.add_variable(variable)
                    # Variable -> BUILD_SET LOAD_CONST SET_UPDATE STORE_FAST
                    elif previous_instructions[0].name == "SET_UPDATE":
                        previous_instructions.append(by[i - 2])
                        previous_instructions.append(by[i - 3])
                        previous_instructions.reverse()
                        # Create a variable object
                        variable = VariableObject()
                        # The current instruction contains the name of variable
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(previous_instructions[1].arg)
                        variable.set_type(str(type(previous_instructions[1].arg).__name__))
                        # Add the variable at variables list:
                        function_object.add_variable(variable)
                    # Import -> LOAD_CONST LOAD_CONST IMPORT_NAME STORE_FAST
                    elif previous_instructions[0].name == "IMPORT_NAME":
                        previous_instructions.append(by[i - 2])
                        previous_instructions.append(by[i - 3])
                        previous_instructions.reverse()
                        # Create an import Object
                        import_object = ImportObject()
                        import_object.add_string(instruction.arg)

                        # Add the import at import list
                        function_object.add_import(import_object)
                    # Import -> LOAD_CONST LOAD_CONST IMPORT_NAME IMPORT_FROM STORE_FAST
                    elif previous_instructions[0].name == "IMPORT_FROM":
                        previous_instructions.append(by[i - 2])
                        previous_instructions.append(by[i - 3])
                        previous_instructions.append(by[i - 4])
                        previous_instructions.reverse()
                        # Create an import Object
                        import_object = ImportObject()
                        import_object.add_string(previous_instructions[1].arg)
                        import_object.set_from_name(previous_instructions[2].arg)

                        # Add the import at import list
                        function_object.add_import(import_object)
                    # Variable -> CallMethod STORE_FAST
                    elif previous_instructions[0].name == "CALL_METHOD":
                        previous_instruction = list()
                        count = i - 1
                        previous_instruction.append(instruction)
                        while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[
                            count].name != "STORE_FAST":
                            previous_instruction.append(by[count])
                            count = count - 1

                        if by[i + 1].name == "CALL_FUNCTION":
                            i = i + 1
                            continue
                        elif by[i + 1].name == "LOAD_METHOD":
                            i = i + 1
                            continue

                        # Create a call function object
                        call_function = CallFunctionObject()

                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                        # Create a variable object
                        variable = VariableObject()

                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(call_function)
                        variable.set_type("CallMethod")

                        # Add the variable at instructions of file object
                        function_object.add_instruction(variable)
                    # Variable -> CallFunction STORE_FAST
                    elif previous_instructions[0].name == "CALL_FUNCTION":
                        previous_instructions.append(by[i - 2])
                        previous_instructions.append(by[i - 3])
                        previous_instructions.append(by[i - 4])
                        previous_instructions.append(by[i - 5])
                        previous_instructions.append(by[i - 6])
                        previous_instructions.reverse()
                        if isinstance(previous_instructions[0].arg, str):
                            previous_instruction = list()
                            count = i - 1
                            previous_instruction.append(instruction)
                            while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[
                                count].name != "STORE_FAST" and by[count].name != "STORE_ATTR":
                                previous_instruction.append(by[count])
                                count = count - 1

                            # Create a call function object
                            call_function = CallFunctionObject()

                            call_function_reader = CallFunctionReader()
                            call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                            # Create a variable object
                            variable = VariableObject()
                            variable.set_variable_name(previous_instruction[0].arg)
                            variable.set_argument(call_function)
                            variable.set_type("CallFunction")

                            # Add the call function at instructions of file object
                            function_object.add_instruction(variable)

                            i = i + 1
                            continue
                    else:
                        print("Not registered")
                        print(instruction)
                        print(previous_instructions[0])
            i = i + 1

        if debug_active == 1:
            print("\n" + function_object.function_name + " End Function Reading...")
