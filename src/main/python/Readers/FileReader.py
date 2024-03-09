from bytecode import bytecode, Label

from Objects.CallFunctionObject import CallFunctionObject
from Objects.CicleObject import CicleObject
from Objects.ClassObject import ClassObject
from Objects.ExceptionObject import ExceptionObject
from Objects.FileObject import FileObject
from Objects.FunctionObject import FunctionObject
from Objects.IfObject import IfObject
from Objects.ImportObject import ImportObject
from Objects.OperationObject import OperationObject
from Objects.VariableObject import VariableObject
from Readers.CallFunctionReader import CallFunctionReader
from Readers.ClassReader import ClassReader
from Readers.FunctionReader import FunctionReader


class FileReader:
    file_directory = ""
    system_object = ""

    def __init__(self, file_directory, system_object):
        self.file_directory = file_directory
        self.system_object = system_object

    def read_file(self, file_object, bytecode_instructions, debug_active):
        if debug_active == 1:
            if isinstance(file_object, CicleObject):
                print("\nCicle Body Reading...")
            else:
                print("\n" + file_object.class_name + " File Reading...")
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
                    false_file_object = FileObject()

                    self.read_file(false_file_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_file_object.get_instructions_list() + false_file_object.get_imports_list() + false_file_object.get_variables_list():
                        exception_object.add_instruction_try(element)

                    # Jump LOAD_CONST RETURN_VALUE <Label> POP_TOP POP_TOP POP_TOP
                    i = i + 6
                    next_instructions = list()
                    while by[i].name != "RETURN_VALUE":
                        next_instructions.append(by[i])
                        i = i + 1
                    next_instructions.append(by[i])

                    # Create a false file object for get all informations
                    false_file_object = FileObject()

                    self.read_file(false_file_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_file_object.get_instructions_list() + false_file_object.get_imports_list() + false_file_object.get_variables_list():
                        exception_object.add_instruction_except(element)

                    # Add exception object at instructions of file
                    file_object.add_instruction(exception_object)

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

                    # Create a false file object for get the instructions
                    false_file_object = FileObject()

                    # Get the objects of instructions
                    self.read_file(false_file_object, instructions_if_true, debug_active)

                    # Add instructions at list
                    for element in false_file_object.get_instructions_list() + false_file_object.get_imports_list() + false_file_object.get_variables_list():
                        if_object.add_instruction_true(element)

                    # Create a false file object for get the instructions
                    false_file_object = FileObject()

                    # Get the objects of instructions
                    self.read_file(false_file_object, instructions_if_false, debug_active)

                    # Add instructions at list
                    for element in false_file_object.get_instructions_list() + false_file_object.get_imports_list() + false_file_object.get_variables_list():
                        if_object.add_instruction_false(element)

                    # Add if at file instructions
                    file_object.add_instruction(if_object)

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

                        # Create a false file object for get the instructions
                        false_file_object = FileObject()

                        # Get the objects of instructions
                        self.read_file(false_file_object, instructions_if_true, debug_active)
                        self.read_file(false_file_object, instructions_if_false, debug_active)

                        # Add instructions at list
                        for element in false_file_object.get_instructions_list() + false_file_object.get_imports_list() + false_file_object.get_variables_list():
                            if_object.add_instruction_true(element)

                        # Add if at file instructions
                        file_object.add_instruction(if_object)

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
                    file_object.add_instruction(call_function)
                # CallFunction -> LOAD_NAME Some informations CALL_FUNCTION
                case "CALL_FUNCTION":
                    previous_instruction = list()
                    count = i - 1
                    previous_instruction.append(instruction)
                    if by[i + 1].name == "GET_ITER":
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
                    elif by[i + 1].name == "STORE_SUBSCR":
                        i = i + 1
                        continue

                    while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[count].name != "STORE_NAME" \
                            and by[count].name != "LOAD_BUILD_CLASS":
                        previous_instruction.append(by[count])
                        count = count - 1

                    # Create a call function object
                    call_function = CallFunctionObject()

                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                    # Add the call function at instructions of file object
                    file_object.add_instruction(call_function)

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
                        print("Condition not registered File Reader", previous_instruction[0])

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
                    self.read_file(cicle_object, body_instructions, debug_active)

                    i = i + 1
                    if not isinstance(by[i], Label):
                        print("GET_ITER ERROR 2")
                    else:
                        i = i + 1

                    # Add cicle at instructions of File Object
                    file_object.add_instruction(cicle_object)

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
                                count].name != "STORE_NAME" and by[count].name != "LOAD_BUILD_CLASS":
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
                                file_object.add_instruction(variable)

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
                        print("STORE_SUBSCR Not registered File Reader")
                        print(previous_instructions[0])

                    # Add the variable at instruction list
                    file_object.add_instruction(variable_object)

                # A Variable Call or import/from keyword
                case "STORE_NAME":
                    previous_instruction = [by[i - 1]]

                    # Class -> LOAD_BUILD_CLASS LOAD_CONST(BodyClass) LOAD_CONST
                    # MAKE_FUNCTION LOAD_CONST CALL_FUNCTION STORE_NAME
                    if previous_instruction[0].name == "CALL_FUNCTION":
                        previous_instruction = list()
                        count = i - 1
                        while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[
                            count].name != "STORE_NAME" and by[count].name != "LOAD_BUILD_CLASS":
                            previous_instruction.append(by[count])
                            count = count - 1
                        previous_instruction.append(by[count])

                        # In this case is a call function
                        if isinstance(previous_instruction[len(previous_instruction) - 2].arg, str):
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
                            file_object.add_instruction(variable)

                            i = i + 1
                            continue

                        # In this other case is a call function
                        if previous_instruction[1].name == "GET_ITER":
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
                            file_object.add_instruction(variable)

                            i = i + 1
                        else:
                            # Create a class object
                            class_object = ClassObject()
                            class_object.set_class_name(instruction.arg)
                            class_object.set_file_name(file_object.get_class_name())

                            # SuperclassList -> LOAD_NAME -> SuperclassList |
                            #                   LOAD_NAME                   |
                            #                   /* empty */
                            for instruction_part in previous_instruction:
                                if instruction_part.name == "LOAD_NAME":
                                    class_object.add_superclass(instruction_part.arg)
                                elif instruction_part.name == "LOAD_CONST" and instruction_part.arg == instruction.arg:
                                    break

                            # Get the bytecode of internal function
                            new_byte = bytecode.Bytecode.from_code(
                                previous_instruction[len(previous_instruction) - 2].arg)

                            # remove the first 4 instructions
                            # BodyClass -> LOAD_NAME STORE_NAME LOAD_CONST STORE_NAME
                            new_byte.pop(0)
                            new_byte.pop(0)
                            new_byte.pop(0)
                            new_byte.pop(0)

                            # Start a class reader for read the body of class
                            class_reader = ClassReader()
                            class_reader.read_class(class_object, new_byte, debug_active)

                            # Add the class at file object
                            file_object.add_class(class_object)
                            # Add the class at the system
                            self.system_object.add_class(class_object)
                    elif previous_instruction[0].name == "CALL_FUNCTION_KW":
                        previous_instruction = list()
                        count = i - 1
                        while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[
                            count].name != "STORE_NAME" and by[count].name != "LOAD_BUILD_CLASS":
                            previous_instruction.append(by[count])
                            count = count - 1
                        previous_instruction.append(by[count])

                        # In this case is a call function
                        if isinstance(previous_instruction[len(previous_instruction) - 1].arg, str):
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
                            file_object.add_instruction(variable)

                            i = i + 1
                            continue
                    # Variable -> CallMethod STORE_NAME
                    elif previous_instruction[0].name == "CALL_METHOD":
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
                        file_object.add_instruction(variable)
                    # Import -> LOAD_CONST LOAD_CONST IMPORT_NAME STORE_NAME
                    elif previous_instruction[0].name == "IMPORT_NAME":
                        previous_instruction.append(by[i - 2])
                        previous_instruction.append(by[i - 3])
                        previous_instruction.reverse()
                        # Create an import Object
                        import_object = ImportObject()
                        import_object.add_string(instruction.arg)
                        # Add the import at import list
                        file_object.add_import(import_object)
                    # Import -> LOAD_CONST LOAD_CONST IMPORT_NAME IMPORT_FROM STORE_NAME
                    elif previous_instruction[0].name == "IMPORT_FROM":
                        previous_instruction.append(by[i - 2])
                        previous_instruction.append(by[i - 3])
                        previous_instruction.append(by[i - 4])
                        previous_instruction.reverse()
                        # Create an import Object
                        import_object = ImportObject()
                        import_object.add_string(previous_instruction[1].arg)
                        import_object.set_from_name(previous_instruction[2].arg)
                        # Add the import at import list
                        file_object.add_import(import_object)
                    # Variable -> BUILD_LIST LOAD_CONST LIST_EXTEND STORE_NAME
                    elif previous_instruction[0].name == "LIST_EXTEND":
                        previous_instruction.append(by[i - 2])
                        previous_instruction.append(by[i - 3])
                        previous_instruction.reverse()
                        # Create a variable object
                        variable = VariableObject()
                        # The current instruction contains the name of variable
                        variable.set_variable_name(instruction.arg)
                        variable.set_type(str(type(previous_instruction[1].arg).__name__))
                        variable.set_argument(previous_instruction[1].arg)
                        # Add the variable at variables list:
                        file_object.add_variable(variable)
                    # Variable -> LOAD_CONST LOAD_CONST BUILD_MAP STORE_NAME
                    elif previous_instruction[0].name == "BUILD_MAP":
                        previous_instruction.append(by[i - 2])
                        previous_instruction.append(by[i - 3])
                        previous_instruction.reverse()
                        # Create a variable object
                        variable = VariableObject()
                        # The current instruction contains the name of variable
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(previous_instruction[0].arg + ":" + previous_instruction[1].arg)
                        variable.set_type("dictionary")
                        # Add the variable at variables list:
                        file_object.add_variable(variable)
                    # Variable -> BUILD_SET LOAD_CONST SET_UPDATE STORE_NAME
                    elif previous_instruction[0].name == "SET_UPDATE":
                        previous_instruction.append(by[i - 2])
                        previous_instruction.append(by[i - 3])
                        previous_instruction.reverse()
                        # Create a variable object
                        variable = VariableObject()
                        # The current instruction contains the name of variable
                        variable.set_variable_name(instruction.arg)
                        variable.set_type(str(type(previous_instruction[1].arg).__name__))
                        variable.set_argument(previous_instruction[1].arg)
                        # Add the variable at variables list:
                        file_object.add_variable(variable)
                    # Variable -> LOAD_CONST STORE_NAME
                    elif previous_instruction[0].name == "LOAD_CONST":
                        variable = VariableObject()
                        # The current instruction contains the name of variable
                        variable.set_variable_name(instruction.arg)
                        variable.set_type(str(type(previous_instruction[0].arg).__name__))
                        variable.set_argument(previous_instruction[0].arg)
                        # Add the variable at variables list:
                        file_object.add_variable(variable)
                    # Function -> LOAD_CONST(InstructionList) LOAD_CONST MAKE_FUNCTION STORE_NAME |
                    #             LOAD_CONST Function                                             |
                    #             LOAD_CONST LOAD_NAME BUILD_TUPLE Function
                    elif previous_instruction[0].name == "MAKE_FUNCTION":
                        previous_instruction.append(by[i - 2])
                        previous_instruction.append(by[i - 3])
                        previous_instruction.append(by[i - 4])
                        previous_instruction.reverse()
                        # Create a function object
                        function = FunctionObject()
                        # The current instruction contains the name of function
                        function.set_function_name(instruction.arg)

                        # Function -> LOAD_CONST Function
                        if previous_instruction[0].name == "LOAD_CONST":
                            # Get the bytecode of internal function
                            new_byte = bytecode.Bytecode.from_code(previous_instruction[1].arg)
                            # Start a function reader for read the internal function
                            function_reader = FunctionReader()
                            function_reader.read_function(function, new_byte, debug_active)
                        # Function -> LOAD_CONST LOAD_NAME BUILD_TUPLE Function
                        elif previous_instruction[0].name == "BUILD_TUPLE":
                            others_instructions = [by[i - 5], by[i - 6]]
                            others_instructions.reverse()
                            # Get the bytecode of internal function
                            new_byte = bytecode.Bytecode.from_code(previous_instruction[1].arg)
                            # Start a function reader for read the internal function
                            function_reader = FunctionReader()
                            function_reader.read_function(function, new_byte, debug_active)
                        # Function -> LOAD_CONST LOAD_NAME BUILD_TUPLE Function
                        else:
                            # Get the bytecode of internal function
                            new_byte = bytecode.Bytecode.from_code(previous_instruction[1].arg)
                            # Start a function reader for read the internal function
                            function_reader = FunctionReader()
                            function_reader.read_function(function, new_byte, debug_active)

                        # This is a constructor case
                        if instruction.arg == "__init__":
                            file_object.set_constructor(function)

                        # Add the function at file object
                        file_object.add_function(function)
                    # Variable -> LOAD_NAME STORE_NAME
                    elif previous_instruction[0].name == "LOAD_NAME":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(previous_instruction[0].arg)
                        file_object.add_instruction(variable)
                    else:
                        print("STORE_NAME not registered File Reader")
                        print(instruction)
                        print(previous_instruction[0])

            i = i + 1
        if debug_active == 1:
            if isinstance(file_object, CicleObject):
                print("Cicle Body End Reading\n")
            else:
                print(file_object.class_name + " End File Reading\n")
