from bytecode import Label, bytecode

from Objects.CallFunctionObject import CallFunctionObject
from Objects.CicleObject import CicleObject
from Objects.ClassObject import ClassObject
from Objects.ExceptionObject import ExceptionObject
from Objects.FunctionObject import FunctionObject
from Objects.IfObject import IfObject
from Objects.ImportObject import ImportObject
from Objects.OperationObject import OperationObject
from Objects.VariableObject import VariableObject
from Readers.CallFunctionReader import CallFunctionReader
from Readers.FunctionReader import FunctionReader


class ClassReader:

    def read_class(self, class_object, bytecode_instructions, debug_active):
        if debug_active == 1:
            if isinstance(class_object, CicleObject):
                print("\nCicle Body Reading...")
            else:
                print("\n" + class_object.class_name + " File Reading...")
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

                # Exception -> SETUP_FINALLY<Label> InstructionList POP_BLOCK InstructionList <Label> POP_TOP POP_TOP
                # POP_TOP InstructionList POP_EXCEPT InstructionList
                case "SETUP_FINALLY":

                    # Create an Exception Object
                    exception_object = ExceptionObject()

                    next_instructions = list()
                    while by[i + 1].name != "RETURN_VALUE":
                        next_instructions.append(by[i + 1])
                        i = i + 1
                    next_instructions.append(by[i + 1])

                    # Create a false file object for get all informations
                    false_class_object = ClassObject()

                    self.read_class(false_class_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_class_object.get_instructions_list() + false_class_object.get_imports_list() + false_class_object.get_variables_list():
                        exception_object.add_instruction_try(element)

                    # Jump LOAD_CONST RETURN_VALUE <Label> POP_TOP POP_TOP POP_TOP
                    i = i + 6
                    next_instructions = list()
                    while by[i].name != "RETURN_VALUE":
                        next_instructions.append(by[i])
                        i = i + 1
                    next_instructions.append(by[i])

                    # Create a false file object for get all informations
                    false_class_object = ClassObject()

                    self.read_class(false_class_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_class_object.get_instructions_list() + false_class_object.get_imports_list() + false_class_object.get_variables_list():
                        exception_object.add_instruction_except(element)

                    # Add exception object at instructions of file
                    class_object.add_instruction(exception_object)

                # If -> Operation POP_JUMP_IF_FALSE InstructionList POP_TOP
                # InstructionList LOAD_CONST RETURN_VALUE <Label> If
                case "POP_JUMP_IF_FALSE":
                    previous_instructions = list()
                    next_instructions = list()
                    previous_instructions.append(by[i - 1])

                    # Create an operation object
                    operation_object = OperationObject()
                    operation_object.set_operation_type(previous_instructions[0].name)
                    # Control the operation type
                    if previous_instructions[0].name == "COMPARE_OP":
                        # First Operand
                        if by[i - 2].name == "LOAD_CONST":
                            operation_object.set_first_operand(
                                str(type(previous_instructions[0].arg).__name__) + ":" + by[i - 2].arg)
                        # Second Operand
                        if by[i - 3].name == "LOAD_CONST":
                            operation_object.set_second_operand(
                                str(type(previous_instructions[0].arg).__name__) + ":" + by[i - 2].arg)
                    else:
                        print(previous_instructions[0])
                        print("Operation not registered")
                    i = i + 1

                    # Create an if object and set the operation
                    if_object = IfObject()
                    if_object.set_operation(operation_object)

                    # Get all instructions
                    while by[i].name != "RETURN_VALUE":
                        next_instructions.append(by[i])
                        i = i + 1
                        if isinstance(by[i], Label):
                            break
                    next_instructions.append(by[i])

                    i = i + 1

                    index = next(i for i, instr in enumerate(next_instructions) if instr.name == 'POP_TOP')

                    instructions_if_true = next_instructions[:index + 1]
                    instructions_if_false = next_instructions[index + 1:]

                    # Create a false class object for get the instructions
                    false_class_object = ClassObject()

                    # Get the objects of instructions
                    self.read_class(false_class_object, instructions_if_true, debug_active)

                    # Add instructions at list
                    for element in false_class_object.get_instructions_list() + false_class_object.get_imports_list() + false_class_object.get_variables_list():
                        if_object.add_instruction_true(element)

                    # Create a false class object for get the instructions
                    false_class_object = ClassObject()

                    # Get the objects of instructions
                    self.read_class(false_class_object, instructions_if_false, debug_active)

                    # Add instructions at list
                    for element in false_class_object.get_instructions_list() + false_class_object.get_imports_list() + false_class_object.get_variables_list():
                        if_object.add_instruction_false(element)

                    # Add if at file instructions
                    class_object.add_instruction(if_object)

                    if isinstance(by[i], Label):
                        i = i + 1

                    count = i
                    next_instructions = list()
                    # Control the next instructions
                    while by[count].name != "RETURN_VALUE":
                        next_instructions.append(by[count])
                        count = count + 1
                        if isinstance(by[count], Label):
                            break
                    next_instructions.append(by[count])
                    operation_list = ["COMPARE_OP", "CONTAINS_OP"]
                    index = next((i for i, instr in enumerate(next_instructions) if instr.name in operation_list), -1)
                    if index == -1:
                        index = next(i for i, instr in enumerate(next_instructions) if instr.name == 'POP_TOP')
                        i = count
                        instructions_if_true = next_instructions[:index + 1]
                        instructions_if_false = next_instructions[index + 1:]

                        # Recreate an if object for else keyword
                        if_object = IfObject()

                        # Create a false class object for get the instructions
                        false_class_object = ClassObject()

                        # Get the objects of instructions
                        self.read_class(false_class_object, instructions_if_true, debug_active)
                        self.read_class(false_class_object, instructions_if_false, debug_active)

                        # Add instructions at list
                        for element in false_class_object.get_instructions_list() + false_class_object.get_imports_list() + false_class_object.get_variables_list():
                            if_object.add_instruction_true(element)

                        # Add if at file instructions
                        class_object.add_instruction(if_object)

                # CallMethod -> LOAD_NAME LOAD_ATTR LOAD_METHOD CALL_METHOD
                case "CALL_METHOD":

                    if by[i + 1].name != "LOAD_METHOD":
                        i = i + 1
                        continue

                    previous_instruction = list()
                    count = i - 1
                    previous_instruction.append(instruction)
                    while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[count].name != "STORE_NAME" \
                            and by[count].name != "STORE_SUBSCR":
                        previous_instruction.append(by[count])
                        count = count - 1

                    # Create a call function object
                    call_function = CallFunctionObject()

                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                    # Add the call function at instructions of file object
                    class_object.add_instruction(call_function)

                # CallFunction -> LOAD_NAME Some informations CALL_FUNCTION
                case "CALL_FUNCTION":

                    if by[i + 1].name == "GET_ITER":
                        i = i + 1
                        continue
                    elif by[i + 1].name == "STORE_SUBSCR":
                        i = i + 1
                        continue
                    elif by[i + 1].name == "STORE_NAME":
                        i = i + 1
                        continue
                    elif by[i + 1].name == "LOAD_METHOD":
                        i = i + 1
                        continue
                    elif by[i + 1].name == "CALL_FUNCTION":
                        i = i + 1
                        continue
                    elif by[i + 1].name == "LOAD_NAME":
                        i = i + 1
                        continue

                    previous_instruction = list()
                    count = i - 1
                    previous_instruction.append(instruction)
                    while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[count].name != "STORE_NAME":
                        previous_instruction.append(by[count])
                        count = count - 1

                    # Create a call function object
                    call_function = CallFunctionObject()

                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                    # Add the call function at instructions of class object
                    class_object.add_instruction(call_function)

                # Cicle -> CallFunction GET_ITER <Label1> FOR_ITER <Label2> STORE_NAME CicleBody
                # JUMP_ABSOLUTE <Label1> <Label2>
                case "GET_ITER":

                    if not isinstance(by[i + 1], Label):
                        if by[i + 1].name == "CALL_FUNCTION":
                            i = i + 1
                            continue

                    previous_instruction = [by[i - 1]]

                    # Create a cicle object
                    cicle_object = CicleObject()

                    # Create a variable for store the condition
                    variable_condition = VariableObject()

                    if previous_instruction[0].name == "CALL_FUNCTION":
                        previous_instruction = list()
                        count = i - 1
                        previous_instruction.append(instruction)
                        while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[count].name != "STORE_NAME" \
                                and by[count].name != "LOAD_BUILD_CLASS" and by[count].name != "RETURN_VALUE":
                            previous_instruction.append(by[count])
                            count = count - 1

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

                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                        variable_condition.set_argument(call_function)
                        variable_condition.set_type("CallFunction")
                    elif previous_instruction[0].name == "LOAD_CONST":
                        variable_condition.set_argument(previous_instruction[0].arg)
                        variable_condition.set_type(str(type(previous_instruction[0].arg).__name__))
                    elif previous_instruction[0].name == "BINARY_SUBSCR":
                        variable_condition.set_argument(by[i - 3].arg + "[" + by[i - 2].arg + "]")
                        variable_condition.set_type("variable")
                    else:
                        print("Condition not registered Class Reader", previous_instruction[0])

                    i = i + 1

                    if not isinstance(by[i], Label):
                        print("GET_ITER ERROR")
                    else:
                        i = i + 1

                    if by[i].name == "FOR_ITER":
                        i = i + 1

                    if by[i].name == "STORE_NAME":
                        variable_condition.set_variable_name(by[i].arg)

                        # Add variable at condition of Cicle Object
                        cicle_object.set_condition(variable_condition)

                        i = i + 1

                    body_instructions = list()
                    while by[i].name != "JUMP_ABSOLUTE":
                        body_instructions.append(by[i])
                        i = i + 1

                    # Call a File Reader for read the instructions of body
                    self.read_class(cicle_object, body_instructions, debug_active)

                    i = i + 1
                    if not isinstance(by[i], Label):
                        print("GET_ITER ERROR 2")
                    else:
                        i = i + 1

                    # Add cicle at instructions of File Object
                    class_object.add_instruction(cicle_object)

                # A variable from dataset called
                case "STORE_ATTR":
                    previous_instruction = [by[i - 1]]

                    # Variable -> CallFunction LOAD_NAME STORE_ATTR
                    if previous_instruction[0].name == "LOAD_NAME":
                        previous_instruction.append(by[i - 2])
                        variable_name = previous_instruction[0].arg + "." + instruction.arg
                        if previous_instruction[1].name == "CALL_FUNCTION":
                            previous_instruction = list()
                            count = i - 1
                            while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[
                                count].name != "STORE_NAME" and by[count].name != "LOAD_BUILD_CLASS" and by[
                                count].name != "RETURN_VALUE":
                                previous_instruction.append(by[count])
                                count = count - 1
                            previous_instruction.append(by[count])

                            # In this case is a call function
                            if isinstance(previous_instruction[len(previous_instruction) - 2].arg, str):
                                # Create a call function object
                                call_function = CallFunctionObject()

                                call_function_reader = CallFunctionReader()
                                call_function_reader.read_call_function(call_function, previous_instruction,
                                                                        debug_active)

                                # Create a variable object
                                variable = VariableObject()
                                variable.set_variable_name(variable_name)
                                variable.set_argument(call_function)
                                variable.set_type("CallFunction")

                                # Add the call function at instructions of file object
                                class_object.add_instruction(variable)

                                i = i + 1
                                continue

                case "STORE_SUBSCR":
                    previous_instructions = list()
                    count = i - 1
                    while by[count].name != "POP_TOP" and by[count].name != "NOP" \
                            and by[count].name != "STORE_NAME" and by[count].name != "LOAD_BUILD_CLASS" \
                            and by[count].name != "RETURN_VALUE":
                        previous_instructions.append(by[count])
                        count = count - 1
                    previous_instructions.append(by[count])

                    # Create a variable objecy for store informations
                    variable_object = VariableObject()

                    # Set the variable name
                    variable_object.set_variable_name(
                        previous_instructions[1].arg + "[" + previous_instructions[0].arg + "]")

                    previous_instructions.remove(previous_instructions[0])
                    previous_instructions.remove(previous_instructions[0])
                    # Variable -> LOAD_CONST LOAD_NAME LOAD_CONST STORE_SUBSCR
                    if previous_instructions[0].name == "LOAD_CONST":
                        variable_object.set_argument(previous_instructions[0].arg)
                        variable_object.set_type(str(type(previous_instructions[0].arg).__name__))
                    # Variable -> LOAD_NAME LOAD_NAME LOAD_CONST STORE_SUBSCR
                    elif previous_instructions[0].name == "LOAD_NAME":
                        variable_object.set_argument(previous_instructions[0].arg)
                        variable_object.set_type("variable")
                    # Variable -> CallMethod LOAD_NAME LOAD_CONST STORE_SUBSCR
                    elif previous_instructions[0].name == "CALL_METHOD":

                        if by[i + 1].name == "CALL_FUNCTION":
                            i = i + 1
                            continue
                        elif by[i + 1].name == "LOAD_METHOD":
                            i = i + 1
                            continue

                        # Create a call function object
                        call_function = CallFunctionObject()

                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, previous_instructions, debug_active)

                        variable_object.set_argument(call_function)
                        variable_object.set_type("CallMethod")
                    else:
                        print("STORE_SUBSCR Not registered Class Reader")
                        print(previous_instructions[0])

                    # Add the variable at instruction list
                    class_object.add_instruction(variable_object)

                case "STORE_NAME":
                    previous_instructions = [by[i - 1]]

                    # Variable -> LOAD_CONST STORE_NAME
                    if previous_instructions[0].name == "LOAD_CONST":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_type(str(type(previous_instructions[0].arg).__name__))
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
                        variable.set_type("variable")
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
                        variable.set_type(str(type(previous_instructions[1].arg).__name__))
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
                        variable.set_type("dictionary")
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
                        variable.set_type(str(type(previous_instructions[1].arg).__name__))
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
                        variable.set_type("CallMethod")

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
                            variable.set_type("CallFunction")

                            # Add the call function at instructions of file object
                            class_object.add_instruction(variable)

                        # In this other case is a call function
                        if previous_instructions[1].name == "GET_ITER":
                            # Create a call function object
                            call_function = CallFunctionObject()
                            call_function_reader = CallFunctionReader()
                            call_function_reader.read_call_function(call_function, previous_instructions, debug_active)

                            # Create a variable object
                            variable = VariableObject()
                            variable.set_variable_name(instruction.arg)
                            variable.set_argument(call_function)
                            variable.set_type("CallFunction")

                            # Add the call function at instructions of file object
                            class_object.add_instruction(variable)

                            i = i + 1
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
                            # Get the bytecode of internal function
                            new_byte = bytecode.Bytecode.from_code(previous_instructions[1].arg)
                            # Start a function reader for read the internal function
                            function_reader = FunctionReader()
                            function_reader.read_function(function, new_byte, debug_active)
                        # Function -> LOAD_CONST LOAD_NAME BUILD_TUPLE Function
                        elif previous_instructions[0].name == "BUILD_TUPLE":
                            others_instructions = [by[i - 5], by[i - 6]]
                            others_instructions.reverse()
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
                        print("STORE_NAME Not registered")
                        print(instruction)
                        print(previous_instructions[0])

            i = i + 1
        if debug_active == 1:
            if isinstance(class_object, CicleObject):
                print("Cicle Body End Reading\n")
            else:
                print(class_object.class_name + " End Class Reading\n")
