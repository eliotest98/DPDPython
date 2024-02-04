from bytecode import Label, bytecode

from Objects.CallFunctionObject import CallFunctionObject
from Objects.FunctionObject import FunctionObject
from Objects.ImportObject import ImportObject
from Objects.VariableObject import VariableObject
from Readers.CallFunctionReader import CallFunctionReader
from Readers.FunctionReader import FunctionReader


class ClassReader:

    def read_class(self, class_object, bytecode_instructions, debug_active):
        if debug_active == 1:
            print("\n" + class_object.class_name + " Class Reading...")
        # Copy for delete instructions when visited
        by = bytecode_instructions

        # remove the first 4 instructions
        # BodyClass -> LOAD_NAME STORE_NAME LOAD_CONST STORE_NAME
        by.pop(0)
        by.pop(0)
        by.pop(0)
        by.pop(0)

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

                # CallMethod -> LOAD_NAME LOAD_ATTR LOAD_METHOD CALL_METHOD
                case "CALL_METHOD":
                    previous_instruction = list()
                    count = i - 1
                    previous_instruction.append(instruction)
                    while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[count].name != "STORE_NAME":
                        previous_instruction.append(by[count])
                        count = count - 1

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
                    elif by[i+1].name == "LOAD_CONST":
                        i = i + 1
                        continue

                    # Create a call function object
                    call_function = CallFunctionObject()

                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                    # Add the call function at instructions of file object
                    class_object.add_instruction(call_function)

                # CallFunction -> LOAD_NAME Some informations CALL_FUNCTION
                case "CALL_FUNCTION":
                    previous_instruction = list()
                    count = i - 1
                    previous_instruction.append(instruction)
                    while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[count].name != "STORE_NAME":
                        previous_instruction.append(by[count])
                        count = count - 1

                    if by[i + 1].name == "STORE_NAME":
                        i = i + 1
                        continue
                    elif by[i+1].name == "LOAD_METHOD":
                        i = i + 1
                        continue

                    # Create a call function object
                    call_function = CallFunctionObject()

                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                    # Add the call function at instructions of class object
                    class_object.add_instruction(call_function)

                case "STORE_NAME":
                    previous_instructions = [by[i - 1]]

                    # Variable -> LOAD_CONST STORE_NAME
                    if previous_instructions[0].name == "LOAD_CONST":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(previous_instructions[0].arg)

                        # Add variabile at variable list of class
                        class_object.add_variable(variable)
                    # Variable -> LOAD_NAME STORE_NAME
                    elif previous_instructions[0].name == "LOAD_NAME":
                        # Create the Variable Object
                        other_variable = VariableObject()
                        other_variable.set_variable_name(previous_instructions[0].arg)
                        # Create the 2* Variable Object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        # Set the 1* Variable Object at 2* Variable Object
                        variable.set_argument(other_variable)
                        # Add the variable at instructions
                        class_object.add_instruction(variable)
                    # Variable -> BUILD_LIST LOAD_CONST LIST_EXTEND STORE_NAME
                    elif previous_instructions[0].name == "LIST_EXTEND":
                        previous_instructions.append(by[i - 2])
                        previous_instructions.append(by[i - 3])
                        previous_instructions.reverse()
                        # Create a variable object
                        variable = VariableObject()
                        # The current instruction contains the name of variable
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(previous_instructions[1].arg)

                        # Add the variable at variables list:
                        class_object.add_variable(variable)
                    # Variable -> LOAD_CONST LOAD_CONST BUILD_MAP STORE_NAME
                    elif previous_instructions[0].name == "BUILD_MAP":
                        previous_instructions.append(by[i - 2])
                        previous_instructions.append(by[i - 3])
                        previous_instructions.reverse()
                        # Create a variable object
                        variable = VariableObject()
                        # The current instruction contains the name of variable
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(previous_instructions[0].arg + ":" + previous_instructions[1].arg)

                        # Add the variable at variables list:
                        class_object.add_variable(variable)
                    # Variable -> BUILD_SET LOAD_CONST SET_UPDATE STORE_NAME
                    elif previous_instructions[0].name == "SET_UPDATE":
                        previous_instructions.append(by[i - 2])
                        previous_instructions.append(by[i - 3])
                        previous_instructions.reverse()
                        # Create a variable object
                        variable = VariableObject()
                        # The current instruction contains the name of variable
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(previous_instructions[1].arg)

                        # Add the variable at variables list:
                        class_object.add_variable(variable)
                    # Variable -> CallMethod STORE_NAME
                    elif previous_instructions[0].name == "CALL_METHOD":
                        previous_instruction = list()
                        count = i - 1
                        previous_instruction.append(instruction)
                        while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[
                            count].name != "STORE_NAME":
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

                        # Add the variable at instructions of file object
                        class_object.add_instruction(variable)
                    # Variable -> CallFunction STORE_FAST
                    elif previous_instructions[0].name == "CALL_FUNCTION":
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
                                count].name != "STORE_NAME":
                                previous_instruction.append(by[count])
                                count = count - 1

                            # Create a call function object
                            call_function = CallFunctionObject()

                            call_function_reader = CallFunctionReader()
                            call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                            # Create a variable object
                            variable = VariableObject()
                            variable.set_variable_name(instruction.arg)
                            variable.set_argument(call_function)

                            # Add the call function at instructions of file object
                            class_object.add_instruction(variable)
                    # Import -> LOAD_CONST LOAD_CONST IMPORT_NAME STORE_NAME
                    elif previous_instructions[0].name == "IMPORT_NAME":
                        previous_instructions.append(by[i - 2])
                        previous_instructions.append(by[i - 3])
                        previous_instructions.reverse()
                        # Create an import Object
                        import_object = ImportObject()
                        import_object.add_string(instruction.arg)

                        # Add the import at import list
                        class_object.add_import(import_object)
                    # Import -> LOAD_CONST LOAD_CONST IMPORT_NAME IMPORT_FROM STORE_NAME
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
                        class_object.add_import(import_object)
                    # Function -> LOAD_CONST(InstructionList) LOAD_CONST MAKE_FUNCTION STORE_NAME |
                    #             LOAD_CONST Function                                             |
                    #             LOAD_CONST LOAD_NAME BUILD_TUPLE Function
                    elif previous_instructions[0].name == "MAKE_FUNCTION":
                        previous_instructions.append(by[i - 2])
                        previous_instructions.append(by[i - 3])
                        previous_instructions.append(by[i - 4])
                        previous_instructions.reverse()
                        # Create a function object
                        function = FunctionObject()
                        # The current instruction contains the name of function
                        function.set_function_name(instruction.arg)

                        # Function -> LOAD_CONST Function
                        if previous_instructions[0].name == "LOAD_CONST":
                            # There is a return value
                            function.set_return_value(previous_instructions[0].arg)
                            # Get the bytecode of internal function
                            new_byte = bytecode.Bytecode.from_code(previous_instructions[1].arg)
                            # Start a function reader for read the internal function
                            function_reader = FunctionReader()
                            function_reader.read_function(function, new_byte, debug_active)
                        # Function -> LOAD_CONST LOAD_NAME BUILD_TUPLE Function
                        elif previous_instructions[0].name == "BUILD_TUPLE":
                            others_instructions = [by[i - 5], by[i - 6]]
                            others_instructions.reverse()
                            # There is type of return value
                            function.set_return_value(
                                others_instructions[0].arg + "(" + others_instructions[1].arg + ")")
                            # Get the bytecode of internal function
                            new_byte = bytecode.Bytecode.from_code(previous_instructions[1].arg)
                            # Start a function reader for read the internal function
                            function_reader = FunctionReader()
                            function_reader.read_function(function, new_byte, debug_active)
                        # Function -> LOAD_CONST LOAD_NAME BUILD_TUPLE Function
                        else:
                            # Get the bytecode of internal function
                            new_byte = bytecode.Bytecode.from_code(previous_instructions[1].arg)
                            # Start a function reader for read the internal function
                            function_reader = FunctionReader()
                            function_reader.read_function(function, new_byte, debug_active)

                        # This is a constructor case
                        if instruction.arg == "__init__":
                            class_object.set_constructor(function)

                        # Add the function at file object
                        class_object.add_function(function)
                    else:
                        print("Not registered")
                        print(instruction)
                        print(previous_instructions[0])

            i = i + 1
        if debug_active == 1:
            print(class_object.class_name + " End File Reading\n")
