import collections.abc

from bytecode import Label, bytecode

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
            if debug_active == 1:
                print(instruction)
            match instruction.name:

                # With -> Condition SETUP_WITH<Label> InstructionList POP_BLOCK
                case "SETUP_WITH":
                    raw_label = str(instruction.arg).removeprefix("<bytecode.instr.Label object at ").removesuffix(">")
                    i = i + 1

                    # Create a with object
                    # TODO

                    next_instructions = list()
                    jump_raw_label = ""
                    while not isinstance(by[i], Label):
                        next_instructions.append(by[i])
                        i = i + 1
                        if isinstance(by[i], Label):
                            internal_raw_label = str(by[i]).removeprefix(
                                "<bytecode.instr.Label object at ").removesuffix(">")
                            if internal_raw_label == raw_label:
                                jump_raw_label = str(by[i - 1].arg).removeprefix(
                                    "<bytecode.instr.Label object at ").removesuffix(">")
                                break
                            next_instructions.append(by[i])
                            i = i + 1

                    # TODO add the instructions at with object

                    next_instructions = list()
                    # Jump Label instruction
                    if isinstance(by[i], Label):
                        i = i + 1

                    while not isinstance(by[i], Label):
                        i = i + 1
                        if isinstance(by[i], Label):
                            internal_raw_label = str(by[i]).removeprefix(
                                "<bytecode.instr.Label object at ").removesuffix(">")
                            if internal_raw_label == jump_raw_label:
                                break
                            i = i + 1

                    # TODO Add with at instructions list

                # Exception -> SETUP_FINALLY<Label> InstructionList POP_BLOCK InstructionList <Label> POP_TOP POP_TOP
                # POP_TOP InstructionList POP_EXCEPT InstructionList
                case "SETUP_FINALLY":

                    raw_label = str(instruction.arg).removeprefix("<bytecode.instr.Label object at ").removesuffix(">")
                    i = i + 1

                    # Create an Exception Object
                    exception_object = ExceptionObject()

                    next_instructions = list()
                    except_raw_label = ""
                    while not isinstance(by[i], Label):
                        next_instructions.append(by[i])
                        i = i + 1
                        if isinstance(by[i], Label):
                            internal_raw_label = str(by[i]).removeprefix(
                                "<bytecode.instr.Label object at ").removesuffix(">")
                            if internal_raw_label == raw_label:
                                except_raw_label = str(by[i - 1].arg).removeprefix(
                                    "<bytecode.instr.Label object at ").removesuffix(">")
                                break
                            next_instructions.append(by[i])
                            i = i + 1

                    # Create a false file object for get all informations
                    false_function_object = FunctionObject()

                    self.read_function(false_function_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_function_object.get_instructions_list() + false_function_object.get_imports_list() + false_function_object.get_variables_list():
                        exception_object.add_instruction_try(element)

                    next_instructions = list()
                    if isinstance(by[i], Label):
                        i = i + 1

                    exception_name = ""
                    if by[i].name == "DUP_TOP":
                        i = i + 1
                        exception_name = by[i].arg
                        i = i + 1

                    if by[i].name == "JUMP_IF_NOT_EXC_MATCH":
                        except_raw_label = str(by[i].arg).removeprefix("<bytecode.instr.Label object at ").removesuffix(
                            ">")

                    while not isinstance(by[i], Label):
                        next_instructions.append(by[i])
                        i = i + 1
                        if len(by) == i:
                            break
                        if isinstance(by[i], Label):
                            internal_raw_label = str(by[i]).removeprefix(
                                "<bytecode.instr.Label object at ").removesuffix(">")
                            if internal_raw_label == except_raw_label:
                                break
                            next_instructions.append(by[i])
                            i = i + 1

                    # Create a false file object for get all informations
                    false_function_object = FunctionObject()

                    self.read_function(false_function_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_function_object.get_instructions_list() + false_function_object.get_imports_list() + false_function_object.get_variables_list():
                        exception_object.add_instruction_except(exception_name, element)

                    if i < len(by):
                        if isinstance(by[i], Label):
                            i = i + 1

                    if i < len(by):
                        if by[i].name == "RERAISE":
                            i = i + 1
                            if i < len(by):
                                if isinstance(by[i], Label):
                                    i = i + 1

                    # Add exception object at instructions of file
                    function_object.add_instruction(exception_object)

                # If -> Operation POP_JUMP_IF_FALSE InstructionList POP_TOP
                # InstructionList LOAD_CONST RETURN_VALUE <Label> If
                case "POP_JUMP_IF_FALSE":
                    raw_label = str(instruction.arg).removeprefix("<bytecode.instr.Label object at ").removesuffix(">")

                    next_instructions = list()

                    copy = by[:i]
                    copy.reverse()
                    return_values = self.arguments_instructions(copy)
                    return_values = self.recursive_identification(return_values[0])
                    # Create an operation object
                    operation_object = return_values[0]

                    i = i + 1

                    # Create an if object and set the operation
                    if_object = IfObject()
                    if_object.set_operation(operation_object)

                    raw_else_label = ""
                    # Get all instructions
                    while not isinstance(by[i], Label):
                        next_instructions.append(by[i])
                        i = i + 1
                        if len(by) == i:
                            break
                        if isinstance(by[i], Label):
                            if_raw_label = str(by[i]).removeprefix(
                                "<bytecode.instr.Label object at ").removesuffix(">")
                            if if_raw_label == raw_label:
                                raw_else_label = str(by[i - 1].arg).removeprefix(
                                    "<bytecode.instr.Label object at ").removesuffix(">")
                                break
                            next_instructions.append(by[i])
                            i = i + 1

                    i = i + 1

                    # Create a false function object for get the instructions
                    false_function_object = FunctionObject()

                    # Get the objects of instructions
                    self.read_function(false_function_object, next_instructions, debug_active)
                    # Add instructions at list
                    for element in false_function_object.get_instructions_list() + false_function_object.get_imports_list() + false_function_object.get_variables_list():
                        if_object.add_instruction_true(element)

                    if not false_function_object.get_return_object().is_empty():
                        if_object.add_instruction_true(false_function_object.get_return_object())

                    if len(by) <= i:
                        continue

                    next_instructions = list()
                    while not isinstance(by[i], Label):
                        # In this case is an elif
                        if by[i].name == "POP_JUMP_IF_FALSE":
                            next_instructions = list()
                            i = i - 1
                            break
                        next_instructions.append(by[i])
                        i = i + 1
                        if len(by) == i:
                            break
                        if isinstance(by[i], Label):
                            else_raw_label = str(by[i]).removeprefix(
                                "<bytecode.instr.Label object at ").removesuffix(">")
                            if else_raw_label == raw_else_label or raw_else_label == "":
                                break
                            next_instructions.append(by[i])
                            i = i + 1

                    # Create a false function object for get the instructions
                    false_function_object = FunctionObject()

                    # Get the objects of instructions
                    self.read_function(false_function_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_function_object.get_instructions_list() + false_function_object.get_imports_list() + false_function_object.get_variables_list():
                        if_object.add_instruction_false(element)

                    if not false_function_object.get_return_object().is_empty():
                        if_object.add_instruction_false(false_function_object.get_return_object())

                    # Add if at file instructions
                    function_object.add_instruction(if_object)

                # If -> Operation POP_JUMP_IF_TRUE InstructionList POP_TOP
                # InstructionList LOAD_CONST RETURN_VALUE <Label> If
                case "POP_JUMP_IF_TRUE":
                    raw_label = str(instruction.arg).removeprefix("<bytecode.instr.Label object at ").removesuffix(">")

                    next_instructions = list()

                    copy = by[:i]
                    copy.reverse()
                    return_values = self.arguments_instructions(copy)
                    return_values = self.recursive_identification(return_values[0])
                    # Create an operation object
                    operation_object = return_values[0]

                    i = i + 1

                    # Create an if object and set the operation
                    if_object = IfObject()
                    if_object.set_operation(operation_object)
                    if_object.set_inverse(True)

                    next_instructions = list()
                    raw_else_label = ""
                    # Get all instructions
                    while not isinstance(by[i], Label):
                        next_instructions.append(by[i])
                        i = i + 1
                        if isinstance(by[i], Label):
                            if_raw_label = str(by[i]).removeprefix(
                                "<bytecode.instr.Label object at ").removesuffix(">")
                            if if_raw_label == raw_label:
                                raw_else_label = str(by[i - 1].arg).removeprefix(
                                    "<bytecode.instr.Label object at ").removesuffix(">")
                                break
                            next_instructions.append(by[i])
                            i = i + 1

                    i = i + 1

                    # Create a false function object for get the instructions
                    false_function_object = FunctionObject()

                    # Get the objects of instructions
                    self.read_function(false_function_object, next_instructions, debug_active)
                    # Add instructions at list
                    for element in false_function_object.get_instructions_list() + false_function_object.get_imports_list() + false_function_object.get_variables_list():
                        if_object.add_instruction_true(element)

                    if not false_function_object.get_return_object().is_empty():
                        if_object.add_instruction_true(false_function_object.get_return_object())

                    next_instructions = list()
                    while not isinstance(by[i], Label):
                        # In this case is an elif
                        if by[i].name == "POP_JUMP_IF_FALSE":
                            next_instructions = list()
                            i = i - 1
                            break
                        next_instructions.append(by[i])
                        i = i + 1
                        if len(by) == i:
                            break
                        if isinstance(by[i], Label):
                            else_raw_label = str(by[i]).removeprefix(
                                "<bytecode.instr.Label object at ").removesuffix(">")
                            if else_raw_label == raw_else_label or raw_else_label == "":
                                break
                            next_instructions.append(by[i])
                            i = i + 1

                    # Create a false function object for get the instructions
                    false_function_object = FunctionObject()

                    # Get the objects of instructions
                    self.read_function(false_function_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_function_object.get_instructions_list() + false_function_object.get_imports_list() + false_function_object.get_variables_list():
                        if_object.add_instruction_false(element)

                    if not false_function_object.get_return_object().is_empty():
                        if_object.add_instruction_false(false_function_object.get_return_object())

                    # Add if at file instructions
                    function_object.add_instruction(if_object)

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
                        expected_load_methods = 1
                        try:
                            while by[count].name != "LOAD_METHOD":
                                if by[count].name == "CALL_METHOD":
                                    expected_load_methods = expected_load_methods + 1
                                previous_instruction.append(by[count])
                                count = count - 1
                                if by[count].name == "LOAD_METHOD":
                                    if expected_load_methods == 1:
                                        previous_instruction.append(by[count])
                                        count = count - 1
                                        break
                                    else:
                                        previous_instruction.append(by[count])
                                        count = count - 1
                                        expected_load_methods = expected_load_methods - 1
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
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)

                        # Create a call function object
                        call_function = CallFunctionObject()

                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, return_values[0], debug_active)

                        return_object = ReturnObject()
                        return_object.set_argument(call_function)
                        return_object.set_type("CallMethod")
                        # Add the variable at instructions of file object
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "LOAD_GLOBAL":
                        # Create a Variable Object
                        variable = VariableObject()
                        variable.set_variable_name(previous_instructions[0].arg)
                        return_object = ReturnObject()
                        return_object.set_type("variable")
                        return_object.set_argument(variable)
                        # Set the return value
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "BINARY_MULTIPLY":
                        variable = VariableObject()
                        variable.set_type("Binary Multiply")
                        variable.set_variable_name(by[i - 3].arg)
                        variable.set_argument(by[i - 2].arg)
                        return_object = ReturnObject()
                        return_object.set_argument(variable)
                        return_object.set_type("lambda")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "LOAD_ATTR":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("CallFunction")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "BINARY_ADD":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("Operation")
                        function_object.set_return_object(return_object)
                    else:
                        print("RETURN_VALUE Not registered Function Reader")
                        print(previous_instructions[0])

                    # End of function
                    if len(by) == i + 1:
                        i = i + 1
                        continue
                    else:
                        if isinstance(by[i + 1], Label):
                            i = i + 2
                            continue

                # CallMethod -> LOAD_FAST LOAD_ATTR LOAD_METHOD CALL_METHOD
                case "CALL_METHOD":

                    if by[i + 1].name != "LOAD_METHOD" and by[i + 1].name != "POP_TOP" and by[
                        i + 1].name != "LOAD_CONST":
                        i = i + 1
                        continue

                    copy = by[:i + 1]
                    copy.reverse()
                    return_values = self.arguments_instructions(copy)
                    previous_instruction = return_values[0]

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

                    copy = by[:i + 1]
                    copy.reverse()
                    return_values = self.arguments_instructions(copy)

                    # Create a call function object
                    call_function = CallFunctionObject()
                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, return_values[0], debug_active)
                    # Add the call function at instructions of function object
                    function_object.add_instruction(call_function)

                # CallFunction -> LOAD_GLOBAL Some informations CALL_FUNCTION
                case "CALL_FUNCTION":

                    if by[i + 1].name != "POP_TOP":
                        i = i + 1
                        continue

                    copy = by[:i + 1]
                    copy.reverse()
                    return_values = self.arguments_instructions(copy)

                    # Create a call function object
                    call_function = CallFunctionObject()

                    # Create a call function object
                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, return_values[0], debug_active)

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

                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)

                        # Create a call function object
                        call_function = CallFunctionObject()

                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, return_values[0], debug_active)

                        variable_condition.set_argument(call_function)
                        variable_condition.set_type("CallFunction")
                    elif previous_instruction[0].name == "LOAD_CONST":
                        variable_condition.set_argument(previous_instruction[0].arg)
                        variable_condition.set_type(str(type(previous_instruction[0].arg).__name__))
                    elif previous_instruction[0].name == "BINARY_SUBSCR":
                        variable_condition.set_argument(by[i - 3].arg + "[" + by[i - 2].arg + "]")
                        variable_condition.set_type("variable")
                    elif previous_instruction[0].name == "CALL_METHOD":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        previous_instruction = return_values[0]

                        # Create a call function object
                        call_function = CallFunctionObject()
                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, previous_instruction, debug_active)
                        # Add the call function at instructions of function object
                        function_object.add_instruction(call_function)

                        # Create a call function object for condtion
                        call_function = CallFunctionObject()

                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                        variable_condition.set_argument(call_function)
                        variable_condition.set_type("CallFunction")
                    elif previous_instruction[0].name == "CALL_FUNCTION_KW":
                        copy = by[:i + 1]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        previous_instruction = return_values[0]

                        # Create a call function object
                        call_function = CallFunctionObject()
                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, previous_instruction, debug_active)
                        # Add the call function at instructions of function object
                        function_object.add_instruction(call_function)

                        # Create a call function object for condtion
                        call_function = CallFunctionObject()

                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                        variable_condition.set_argument(call_function)
                        variable_condition.set_type("CallFunction")
                    elif previous_instruction[0].name == "LOAD_FAST":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable_condition.set_argument(return_values[0])
                        variable_condition.set_type("variable")
                    else:
                        print("Condition not registered")
                        print(previous_instruction[0])

                    i = i + 1
                    if not isinstance(by[i], Label):
                        print("GET_ITER ERROR")
                    else:
                        i = i + 1

                    label_esadecimal = ""
                    if by[i].name == "FOR_ITER":
                        label_esadecimal = str(by[i].arg).removeprefix("<bytecode.instr.Label object at ").removesuffix(
                            ">")
                        i = i + 1

                    if by[i].name == "STORE_NAME" or by[i].name == "STORE_FAST":
                        variable_condition.set_variable_name(by[i].arg)

                        # Add variable at condition of Cicle Object
                        cicle_object.set_condition(variable_condition)

                        i = i + 1

                    body_instructions = list()
                    while not isinstance(by[i], Label):
                        body_instructions.append(by[i])
                        i = i + 1
                        if isinstance(by[i], Label):
                            for_label_esadecimal = str(by[i]).removeprefix(
                                "<bytecode.instr.Label object at ").removesuffix(
                                ">")
                            if for_label_esadecimal == label_esadecimal:
                                break
                            else:
                                body_instructions.append(by[i])
                                i = i + 1

                    # Call a File Reader for read the instructions of body
                    fake_function_object = FunctionObject()
                    self.read_function(fake_function_object, body_instructions, debug_active)

                    for instruction in fake_function_object.get_instructions_list():
                        cicle_object.add_instruction(instruction)

                    i = i + 1
                    if isinstance(by[i], Label):
                        i = i + 1

                    # Add cicle at instructions of File Object
                    function_object.add_instruction(cicle_object)

                case "STORE_SUBSCR":

                    copy = by[:i + 1]
                    copy.reverse()
                    return_values = self.arguments_instructions(copy)
                    previous_instructions = return_values[0]
                    previous_instructions.remove(previous_instructions[0])
                    square_parenthesis = previous_instructions[0].arg
                    previous_instructions.remove(previous_instructions[0])
                    variable_name = previous_instructions[0].arg
                    previous_instructions.remove(previous_instructions[0])

                    # Create a variable objecy for store informations
                    variable_object = VariableObject()

                    # Set the variable name
                    variable_object.set_variable_name(
                        variable_name + "[" + str(square_parenthesis) + "]")

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
                        # Create a call function object
                        call_function = CallFunctionObject()

                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, previous_instructions, debug_active)

                        variable_object.set_argument(call_function)
                        variable_object.set_type("CallMethod")
                    elif previous_instructions[0].name == "LOAD_FAST":
                        return_values = self.arguments_instructions(previous_instructions)
                        return_values = self.recursive_identification(return_values[0])
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("CallFunction")
                    elif previous_instructions[0].name == "BINARY_ADD":
                        return_values = self.arguments_instructions(previous_instructions)
                        return_values = self.recursive_identification(return_values[0])
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("Operation")
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
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        previous_instruction = return_values[0]

                        # Create a call function object
                        call_function = CallFunctionObject()
                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, previous_instruction, debug_active)
                        # Add the call function at instructions of function object
                        function_object.add_instruction(call_function)

                        # Create a call function object for condtion
                        call_function = CallFunctionObject()

                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, previous_instruction, debug_active)

                        variable = VariableObject()
                        variable.set_argument(call_function)
                        variable.set_type("CallFunction")

                        # Add the call function at instructions of file object
                        function_object.add_instruction(variable)

                        i = i + 1
                        continue
                    elif previous_instructions[0].name == "MAKE_FUNCTION":
                        # Create a function object
                        function = FunctionObject()
                        # The current instruction contains the name of function
                        function.set_function_name(instruction.arg)
                        # Function -> LOAD_CONST Function
                        if by[i - 2].name == "LOAD_CONST":
                            # Get the bytecode of internal function
                            new_byte = bytecode.Bytecode.from_code(by[i - 3].arg)
                            # Start a function reader for read the internal function
                            function_reader = FunctionReader()
                            function_reader.read_function(function, new_byte, debug_active)

                            # Add the function at file object
                            function_object.add_lambda_function(function)
                    elif previous_instructions[0].name == "BINARY_SUBSCR":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)

                        # Get the previous instructions
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "BINARY_ADD":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_type("Operation")

                        # Get the previous instructions
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "UNPACK_SEQUENCE":
                        # Create a Variable Object
                        variable_object = VariableObject()
                        variable_object.set_variable_name(instruction.arg)
                        variable_object.set_type("VariableSequence")
                        arguments = ""
                        number_of_arguments = previous_instructions[0].arg
                        counter_arguments = 0
                        while counter_arguments < number_of_arguments:
                            arguments = arguments + by[i].arg + ","
                            i = i + 1
                            counter_arguments = counter_arguments + 1

                        variable_object.set_argument(arguments.removesuffix(","))

                        # Add the variable at variable list
                        function_object.add_variable(variable_object)
                    else:
                        print("STORE_FAST Function Reader Not registered")
                        print(previous_instructions[0])
            i = i + 1

        if debug_active == 1:
            if isinstance(function_object, CicleObject):
                print("Cicle Body End Reading\n")
            else:
                print(function_object.function_name + " End Function Reading\n")

    def recursive_identification(self, by):
        counter = 0
        if isinstance(by, collections.abc.Sequence):
            if by[counter].name == "LOAD_CONST":
                value = by[counter].arg
                counter = counter + 1
                return value, by[counter:]
            elif by[counter].name == "LOAD_NAME":
                value = by[counter].arg
                counter = counter + 1
                return value, by[counter:]
            elif by[counter].name == "LOAD_ATTR":
                second_value = by[counter].arg
                counter = counter + 1
                return_values = self.recursive_identification(by[counter:])
                first_value = return_values[0]
                by = return_values[1]
                counter = 0
                return str(first_value) + "." + str(second_value), by[counter:]
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
            elif by[counter].name == "LOAD_FAST":
                value = by[counter].arg
                counter = counter + 1
                variable = VariableObject()
                variable.set_variable_name(value)
                variable.set_type("variable")
                return variable, by[counter:]
            elif by[counter].name == "LOAD_GLOBAL":
                value = by[counter].arg
                counter = counter + 1
                return value, by[counter:]
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
                # TODO i don't know if is forever
                if by[counter].name == "LOAD_METHOD":
                    return_values = self.recursive_identification(by[counter:])
                    call_function.set_method_name("." + return_values[0])
                    by = return_values[1]
                    counter = 0
                else:
                    print("LOAD_METHOD not forever")
                    print(by)
                    exit(-1)

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
            elif by[counter].name == "LOAD_METHOD":
                value = by[counter].arg
                counter = counter + 1
                return value, by[counter:]
            elif by[counter].name == "BINARY_ADD":
                counter = counter + 1

                # First Operand
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                sum = " + " + str(return_values[0])

                # Second Operand
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                sum = str(return_values[0]) + sum

                return sum, by[counter:]
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
            else:
                print("Recursive identification not registered Function Reader")
                print(by[counter])
                exit(-1)
        else:
            if by.name == "LOAD_FAST":
                value = by.arg
                variable = VariableObject()
                variable.set_variable_name(value)
                variable.set_type("variable")
                return variable, []
            else:
                print("Recursive identification not registered Function Reader Single")
                print(by)
                exit(-1)

    # return_values[0] = instruction/instruction list return_values[1] = bytecode modified
    def arguments_instructions(self, by):
        counter = 0
        if by[counter].name == "LOAD_CONST" or by[counter].name == "LOAD_FAST" or by[counter].name == "LOAD_GLOBAL" \
                or by[counter].name == "LOAD_METHOD" or by[counter].name == "STORE_FAST" \
                or by[counter].name == "LOAD_CLOSURE":
            value = by[counter]
            counter = counter + 1
            return value, by[counter:]
        elif by[counter].name == "LOAD_ATTR":
            instruction_list = list()
            instruction_list.append(by[counter])
            counter = counter + 1
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            return instruction_list, by[counter:]
        elif by[counter].name == "BUILD_MAP":
            instruction_list = list()
            instruction_list.append(by[counter])
            number_of_arguments = by[counter].arg
            counter = counter + 1
            arguments_counter = 0
            while arguments_counter < number_of_arguments:
                # Value
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])
                by = return_values[1]
                counter = 0
                # Key
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])
                by = return_values[1]
                counter = 0
                arguments_counter = arguments_counter + 1
            return instruction_list, by[counter:]
        elif by[counter].name == "CALL_FUNCTION_KW":
            instruction_list = list()
            number_of_arguments = by[counter].arg
            instruction_list.append(by[counter])
            counter = counter + 1
            # Parameters List
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0

            counter_arguments = 0
            # Parameters
            while counter_arguments < number_of_arguments:
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])

                by = return_values[1]
                counter = 0
                counter_arguments = counter_arguments + 1

            # Function Name
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0

            return instruction_list, by[counter:]
        elif by[counter].name == "BINARY_SUBSCR" or by[counter].name == "BINARY_ADD" \
                or by[counter].name == "BINARY_SUBTRACT":
            instruction_list = list()
            instruction_list.append(by[counter])
            counter = counter + 1
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            return instruction_list, by[counter:]
        elif by[counter].name == "GET_ITER":
            instruction_list = list()
            instruction_list.append(by[counter])
            counter = counter + 1

            # Condition
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0

            # Body
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            return instruction_list, by[counter:]
        elif by[counter].name == "CALL_METHOD":
            instruction_list = list()
            instruction_list.append(by[counter])
            number_of_arguments = by[counter].arg
            counter_arguments = 0
            counter = counter + 1

            # Parameters
            while counter_arguments < number_of_arguments:
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])
                by = return_values[1]
                counter = 0
                counter_arguments = counter_arguments + 1

            # Name of method
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0

            # Path of method
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            return instruction_list, by[counter:]
        elif by[counter].name == "CALL_FUNCTION":
            instruction_list = list()
            instruction_list.append(by[counter])
            number_of_arguments = by[counter].arg
            counter_arguments = 0
            counter = counter + 1

            # Parameters
            while counter_arguments < number_of_arguments:
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])
                by = return_values[1]
                counter = 0
                counter_arguments = counter_arguments + 1

            instructions = by[counter:]
            if len(instructions) != 0:
                return_values = self.arguments_instructions(instructions)
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])
                by = return_values[1]
                counter = 0
            return instruction_list, by[counter:]
        elif by[counter].name == "BUILD_LIST":
            instruction_list = list()
            instruction_list.append(by[counter])
            number_of_elements = by[counter].arg
            counter = counter + 1
            arguments_counter = 0
            while arguments_counter < number_of_elements:
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])
                by = return_values[1]
                counter = 0
                arguments_counter = arguments_counter + 1

            return instruction_list, by[counter:]
        elif by[counter].name == "MAKE_FUNCTION":
            instruction_list = list()
            instruction_list.append(by[counter])
            counter = counter + 1

            # Function Name
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0

            # Bytecode
            instruction_list.append(by[counter].arg)
            counter = counter + 1
            return instruction_list, by[counter:]
        elif by[counter].name == "BUILD_TUPLE":
            instruction_list = list()
            number_of_arguments = by[counter].arg
            instruction_list.append(by[counter])
            counter = counter + 1
            arguments_counter = 0
            while arguments_counter < number_of_arguments:
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])
                by = return_values[1]
                counter = 0
                arguments_counter = arguments_counter + 1

            return instruction_list, by[counter:]
        elif by[counter].name == "STORE_SUBSCR":
            instruction_list = list()
            # Current Instruction
            instruction_list.append(by[counter])
            counter = counter + 1

            # Variable Left Part

            # LOAD_CONST Instruction
            instruction_list.append(by[counter])
            counter = counter + 1
            # LOAD_NAME Instruction
            instruction_list.append(by[counter])
            counter = counter + 1

            # Variable Right Part
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            return instruction_list, by[counter:]
        elif by[counter].name.__contains__("_OP"):
            instruction_list = list()
            instruction_list.append(by[counter])
            counter = counter + 1
            # First Operand
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            # Second Operand
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            return instruction_list, by[counter:]
        elif by[counter].name == "BUILD_SLICE":
            instruction_list = list()
            number_of_arguments = by[counter].arg
            instruction_list.append(by[counter])
            counter = counter + 1
            arguments_counter = 0
            # Arguments
            while arguments_counter < number_of_arguments:
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])
                by = return_values[1]
                counter = 0
                arguments_counter = arguments_counter + 1

            # Slice Name
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])

            return instruction_list, by[counter:]
        elif by[counter].name == "BINARY_MODULO":
            instruction_list = list()
            instruction_list.append(by[counter])
            counter = counter + 1
            # First Part
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            # Second Part
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            return instruction_list, by[counter:]
        else:
            print("Arguments instructions not registered")
            print(by[counter])
            exit(-1)
