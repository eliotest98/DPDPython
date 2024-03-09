from bytecode import Label

from Objects.CallFunctionObject import CallFunctionObject
from Objects.CicleObject import CicleObject
from Objects.ClassObject import ClassObject
from Objects.ExceptionObject import ExceptionObject
from Objects.FunctionObject import FunctionObject
from Objects.IfObject import IfObject
from Objects.ImportObject import ImportObject
from Objects.OperationObject import OperationObject
from Objects.ReturnObject import ReturnObject
from Objects.VariableObject import VariableObject
from Readers.CallFunctionReader import CallFunctionReader


class FunctionReader:

    def read_function(self, function_object, bytecode_instructions, debug_active):
        if debug_active == 1:
            if isinstance(function_object, CicleObject):
                print("\nCicle Body Reading...")
            else:
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

                # Exception -> SETUP_FINALLY<Label> InstructionList POP_BLOCK InstructionList <Label> POP_TOP POP_TOP
                # POP_TOP InstructionList POP_EXCEPT InstructionList
                case "SETUP_FINALLY":

                    # Create an Exception Object
                    exception_object = ExceptionObject()

                    next_instructions = list()
                    while by[i + 1].name != "RETURN_VALUE" and by[i].name != "POP_BLOCK":
                        next_instructions.append(by[i + 1])
                        i = i + 1
                    next_instructions.append(by[i + 1])

                    # Create a false file object for get all informations
                    false_function_object = FunctionObject()

                    self.read_function(false_function_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_function_object.get_instructions_list() + false_function_object.get_imports_list() + false_function_object.get_variables_list():
                        exception_object.add_instruction_try(element)

                    # Jump LOAD_CONST RETURN_VALUE <Label> POP_TOP POP_TOP POP_TOP
                    i = i + 6
                    next_instructions = list()
                    if i >= len(by):
                        continue
                    while by[i].name != "RETURN_VALUE":
                        next_instructions.append(by[i])
                        i = i + 1
                        if isinstance(by[i], Label):
                            next_instructions.append(by[i])
                            i = i + 1
                    next_instructions.append(by[i])

                    # Create a false file object for get all informations
                    false_function_object = FunctionObject()

                    self.read_function(false_function_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_function_object.get_instructions_list() + false_function_object.get_imports_list() + false_function_object.get_variables_list():
                        exception_object.add_instruction_except(element)

                    # Add exception object at instructions of file
                    function_object.add_instruction(exception_object)

                    # If the statement is at end of function i add the last two instructions
                    if len(by) == i + 1:
                        by.append(by[i - 1])
                        by.append(by[i])

                # If -> Operation POP_JUMP_IF_FALSE InstructionList POP_TOP
                # InstructionList LOAD_CONST RETURN_VALUE <Label> If
                case "POP_JUMP_IF_FALSE":
                    previous_instructions = list()
                    next_instructions = list()
                    previous_instructions.append(by[i - 1])

                    # Create an operation object
                    operation_object = OperationObject()

                    # Counter for operations
                    count = i - 1

                    if previous_instructions[0].name.__contains__("OP"):
                        operation_object.set_operation_type(previous_instructions[0].name)
                        count = count - 1
                        # First Operand
                        if by[count].name == "LOAD_CONST":
                            operation_object.set_first_operand(
                                str(type(by[count].arg).__name__) + ":" + by[count].arg)
                        elif by[count].name == "LOAD_ATTR":
                            index = count - 1
                            variable_object = VariableObject()
                            variable_object.set_variable_name(by[index].arg + "." + by[count].arg)
                            variable_object.set_type("variable")
                            operation_object.set_first_operand(variable_object)
                            count = count - 1
                        elif by[count].name == "LOAD_FAST":
                            variable_object = VariableObject()
                            variable_object.set_variable_name(by[count].arg)
                            operation_object.set_first_operand(variable_object)
                        else:
                            print("Operand not registered Function Reader")
                            print(by[count])
                        count = count - 1
                        # Second Operand
                        if by[count].name == "LOAD_CONST":
                            operation_object.set_second_operand(
                                str(type(by[count].arg).__name__) + ":" + by[count].arg)
                        elif by[count].name == "LOAD_ATTR":
                            index = count - 1
                            variable_object = VariableObject()
                            variable_object.set_variable_name(by[index].arg + "." + by[count].arg)
                            variable_object.set_type("variable")
                            operation_object.set_second_operand(variable_object)
                            count = count - 1
                        elif by[count].name == "LOAD_FAST":
                            variable_object = VariableObject()
                            variable_object.set_variable_name(by[count].arg)
                            operation_object.set_first_operand(variable_object)
                        else:
                            print("Operand not registered")
                            print(by[count])
                    i = i + 1

                    # Create an if object and set the operation
                    if_object = IfObject()
                    if_object.set_operation(operation_object)

                    # Get all instructions
                    while by[i].name != "RETURN_VALUE":
                        next_instructions.append(by[i])
                        i = i + 1
                        if isinstance(by[i], Label):
                            next_instructions.append(by[i])
                            i = i + 1
                        if i >= len(by):
                            break
                    try:
                        next_instructions.append(by[i])
                    except:
                        pass

                    i = i + 1

                    index = next((i for i, instr in enumerate(next_instructions) if
                                  not isinstance(instr, Label) and instr.name == 'POP_TOP'), -1)

                    instructions_if_false = []
                    if index == - 1:
                        instructions_if_true = next_instructions
                    else:
                        instructions_if_true = next_instructions[index + 1:]
                        instructions_if_false = next_instructions[:index + 1]

                    # Create a false function object for get the instructions
                    false_function_object = FunctionObject()

                    # Get the objects of instructions
                    self.read_function(false_function_object, instructions_if_true, debug_active)
                    # Add instructions at list
                    for element in false_function_object.get_instructions_list() + false_function_object.get_imports_list() + false_function_object.get_variables_list():
                        if_object.add_instruction_true(element)

                    if len(instructions_if_false) == 1:
                        continue

                    # Create a false function object for get the instructions
                    false_function_object = FunctionObject()

                    # Get the objects of instructions
                    self.read_function(false_function_object, instructions_if_false, debug_active)

                    # Add instructions at list
                    for element in false_function_object.get_instructions_list() + false_function_object.get_imports_list() + false_function_object.get_variables_list():
                        if_object.add_instruction_false(element)

                    # Add if at file instructions
                    function_object.add_instruction(if_object)

                    if i >= len(by):
                        continue

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
                    if not isinstance(by[count], Label):
                        next_instructions.append(by[count])
                    operation_list = ["COMPARE_OP", "CONTAINS_OP"]
                    index = next((i for i, instr in enumerate(next_instructions) if instr.name in operation_list), -1)
                    if index == -1:
                        index = next((i for i, instr in enumerate(next_instructions) if instr.name == 'POP_TOP'), -1)
                        if index == - 1:
                            continue
                        i = count
                        instructions_if_true = next_instructions[index + 1:]
                        instructions_if_false = next_instructions[:index + 1]

                        # Recreate an if object for else keyword
                        if_object = IfObject()

                        # Create a false function object for get the instructions
                        false_function_object = FunctionObject()

                        # Get the objects of instructions
                        self.read_function(false_function_object, instructions_if_true, debug_active)
                        self.read_function(false_function_object, instructions_if_false, debug_active)

                        # Add instructions at list
                        for element in false_function_object.get_instructions_list() + false_function_object.get_imports_list() + false_function_object.get_variables_list():
                            if_object.add_instruction_true(element)

                        # Add if at file instructions
                        function_object.add_instruction(if_object)

                        # If the statement is at end of function i add the last two instructions
                        if len(by) == i + 1:
                            by.append(by[i - 1])
                            by.append(by[i])

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
                    # ReturnValue -> CALL_FUNCTION RETURN_VALUE
                    elif previous_instructions[0].name == "CALL_FUNCTION":
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
                        print("RETURN_VALUE Not registered")
                        print(instruction)
                        print(previous_instructions[0])

                # CallMethod -> LOAD_FAST LOAD_ATTR LOAD_METHOD CALL_METHOD
                case "CALL_METHOD":

                    if by[i + 1].name != "LOAD_METHOD" and by[i + 1].name != "POP_TOP":
                        i = i + 1
                        continue

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

                    # Create a call function object
                    call_function = CallFunctionObject()

                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                    # Add the call function at instructions of file object
                    function_object.add_instruction(call_function)

                # CallFunction -> LOAD_GLOBAL Some informations CALL_FUNCTION
                case "CALL_FUNCTION_KW":

                    if by[i + 1].name != "POP_TOP":
                        i = i + 1
                        continue

                    previous_instruction = list()
                    count = i - 1
                    previous_instruction.append(instruction)
                    while by[count].name != "LOAD_GLOBAL" and by[count].name != "RETURN_VALUE" and by[
                        count].name != "POP_TOP":
                        previous_instruction.append(by[count])
                        count = count - 1
                    previous_instruction.append(by[count])

                    # Create a call function object
                    call_function = CallFunctionObject()

                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                    # Add the call function at instructions of function object
                    function_object.add_instruction(call_function)

                # CallFunction -> LOAD_GLOBAL Some informations CALL_FUNCTION
                case "CALL_FUNCTION":

                    if by[i + 1].name != "POP_TOP":
                        i = i + 1
                        continue

                    previous_instruction = list()
                    count = i - 1
                    previous_instruction.append(instruction)
                    if by[count].name == "LOAD_GLOBAL":
                        previous_instruction.append(by[count])
                        count = count - 1
                    while by[count].name != "LOAD_GLOBAL" and by[count].name != "RETURN_VALUE":
                        previous_instruction.append(by[count])
                        count = count - 1
                    previous_instruction.append(by[count])

                    # Create a call function object
                    call_function = CallFunctionObject()

                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, previous_instruction, debug_active)
                    # Add the call function at instructions of function object
                    function_object.add_instruction(call_function)

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
                    elif previous_instruction[0].name == "CALL_FUNCTION_KW":
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
                    else:
                        print("Condition not registered", previous_instruction[0])

                    i = i + 1
                    if not isinstance(by[i], Label):
                        print("GET_ITER ERROR")
                    else:
                        i = i + 1

                    if by[i].name == "FOR_ITER":
                        i = i + 1

                    if by[i].name == "STORE_NAME" or by[i].name == "STORE_FAST":
                        variable_condition.set_variable_name(by[i].arg)

                        # Add variable at condition of Cicle Object
                        cicle_object.set_condition(variable_condition)

                        i = i + 1

                    body_instructions = list()
                    while by[i].name != "JUMP_ABSOLUTE":
                        body_instructions.append(by[i])
                        i = i + 1
                        if isinstance(by[i], Label):
                            body_instructions.append(by[i])
                            i = i + 1
                    print(body_instructions)

                    # Call a File Reader for read the instructions of body
                    self.read_function(cicle_object, body_instructions, debug_active)

                    i = i + 1
                    if not isinstance(by[i], Label):
                        print("GET_ITER ERROR 2")
                    else:
                        i = i + 1

                    # Add cicle at instructions of File Object
                    function_object.add_instruction(cicle_object)

                case "STORE_SUBSCR":
                    previous_instructions = list()
                    count = i - 1
                    while by[count].name != "POP_TOP" and by[count].name != "NOP" \
                            and by[count].name != "STORE_NAME" and by[count].name != "LOAD_BUILD_CLASS" \
                            and by[count].name != "RETURN_VALUE" and by[count].name != "STORE_FAST" \
                            and by[count].name != "STORE_SUBSCR":
                        print(previous_instructions)
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
                        if len(by) != i + 1:
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
                    # Variable -> CallFunction LOAD_NAME LOAD_CONST STORE_SUBSCR
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
                                if isinstance(by[count], Label):
                                    break

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

                        previous_instructions.reverse()
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
                            function_object.add_instruction(variable)

                            i = i + 1
                    else:
                        print("STORE_SUBSCR Not registered")
                        print(previous_instructions[0])

                    # Add the variable at instruction list
                    function_object.add_instruction(variable_object)

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
                                    print(previous_instructions)
                                    previous_instruction.append(by[count])
                                    count = count - 1
                                    if isinstance(by[count], Label):
                                        break

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

                            # In this other case is a call function
                            if previous_instructions[1].name == "GET_ITER":
                                print("Entra?")
                                # Create a call function object
                                call_function = CallFunctionObject()
                                call_function_reader = CallFunctionReader()
                                call_function_reader.read_call_function(call_function, previous_instructions,
                                                                        debug_active)

                                # Create a variable object
                                variable = VariableObject()
                                variable.set_variable_name(instruction.arg)
                                variable.set_argument(call_function)
                                variable.set_type("CallFunction")

                                # Add the call function at instructions of file object
                                function_object.add_instruction(variable)

                                i = i + 1
                        else:
                            print("STORE_ATTR Not registered")
                            print(instruction)
                            print(previous_instructions[0])
                            print(previous_instructions[1])
                    elif previous_instructions[0].name == "LOAD_GLOBAL":
                        previous_instructions.append(by[i - 2])
                        if previous_instructions[1].name == "CALL_FUNCTION":
                            variable_name = previous_instructions[0].arg + "." + instruction.arg
                            previous_instructions = list()
                            count = i - 1
                            while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[
                                count].name != "STORE_NAME" and by[count].name != "LOAD_BUILD_CLASS" and by[
                                count].name != "RETURN_VALUE":
                                previous_instructions.append(by[count])
                                count = count - 1
                                if isinstance(by[count], Label):
                                    break
                            previous_instructions.append(by[count])

                            # In this case is a call function
                            if isinstance(previous_instructions[len(previous_instructions) - 2].arg, str):
                                # Create a call function object
                                call_function = CallFunctionObject()

                                call_function_reader = CallFunctionReader()
                                call_function_reader.read_call_function(call_function, previous_instructions,
                                                                        debug_active)

                                # Create a variable object
                                variable = VariableObject()
                                variable.set_variable_name(variable_name)
                                variable.set_argument(call_function)
                                variable.set_type("CallFunction")

                                # Add the call function at instructions of file object
                                function_object.add_instruction(variable)

                                i = i + 1
                                continue
                    else:
                        print("External STORE_ATTR Not registered")
                        print("Current instruction ", instruction)
                        print("Previous instruction ", previous_instructions[0])

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
                            if isinstance(by[count], Label):
                                break

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
                                if isinstance(by[count], Label):
                                    break

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

                        previous_instructions.reverse()
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
                            function_object.add_instruction(variable)

                            i = i + 1
                    # Variable -> LOAD_CONST BUILD_LIST STORE_FAST
                    elif previous_instructions[0].name == "BUILD_LIST":
                        variable_object = VariableObject()
                        variable_object.set_variable_name(instruction.arg)
                        variable_object.set_type("list")
                        number_of_elements = previous_instructions[0].arg
                        count = 0
                        arguments = ""
                        while count < number_of_elements:
                            arguments = arguments + by[i - 2].arg + ","
                            count = count + 1
                        variable_object.set_argument(arguments.removesuffix(","))
                        function_object.add_variable(variable_object)
                    # Variable -> CallFunction STORE_FAST
                    elif previous_instructions[0].name == "CALL_FUNCTION_KW":
                        previous_instructions = list()
                        count = i - 1
                        while by[count].name != "POP_TOP" and by[count].name != "NOP" and by[
                            count].name != "STORE_NAME" and by[count].name != "LOAD_BUILD_CLASS":
                            previous_instructions.append(by[count])
                            count = count - 1
                            if count < 0:
                                break
                            if isinstance(by[count], Label):
                                previous_instructions.append(by[count])
                                count = count - 1
                        previous_instructions.append(by[count])

                        # In this case is a call function
                        if isinstance(previous_instructions[len(previous_instructions) - 1].arg, str):
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
                            function_object.add_instruction(variable)

                            i = i + 1
                            continue
                    elif previous_instructions[0].name == "BINARY_SUBSCR":
                        variable_object = VariableObject()
                        variable_object.set_argument(by[i - 3].arg + "[" + by[i - 2].arg + "]")
                        variable_object.set_type("variable")
                        function_object.add_instruction(variable_object)
                    else:
                        print("STORE_FAST Not registered")
                        print(instruction)
                        print(previous_instructions[0])
            i = i + 1

        if debug_active == 1:
            if isinstance(function_object, CicleObject):
                print("Cicle Body End Reading\n")
            else:
                print(function_object.function_name + " End Function Reading\n")
