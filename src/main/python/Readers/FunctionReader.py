import collections.abc

from bytecode import Label, bytecode, Instr

from Objects.CallFunctionObject import CallFunctionObject
from Objects.CicleObject import CicleObject
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
            if isinstance(instruction, Label):
                i = i + 1
                continue
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
                        if i >= len(by):
                            break
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

                # If -> Operation JUMP_IF_TRUE_OR_POP InstructionList POP_TOP
                # InstructionList LOAD_CONST RETURN_VALUE <Label> If
                case "JUMP_IF_TRUE_OR_POP":
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
                                if isinstance(next_instructions[len(next_instructions) - 1].arg, Label):
                                    raw_else_label = str(by[i - 1].arg).removeprefix(
                                        "<bytecode.instr.Label object at ").removesuffix(">")
                                    next_instructions.remove(next_instructions[len(next_instructions) - 1])
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

                    if len(by) <= i or raw_else_label == "":
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

                    if len(by) == i:
                        # Add if at file instructions
                        function_object.add_instruction(operation_object)
                        continue

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
                                if isinstance(next_instructions[len(next_instructions) - 1].arg, Label):
                                    raw_else_label = str(by[i - 1].arg).removeprefix(
                                        "<bytecode.instr.Label object at ").removesuffix(">")
                                    next_instructions.remove(next_instructions[len(next_instructions) - 1])
                                break
                            next_instructions.append(by[i])
                            i = i + 1
                            if len(by) == i:
                                break

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

                    if len(by) <= i or raw_else_label == "":
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

                    # Assert condition
                    if len(by) == i:
                        # Add if at file instructions
                        function_object.add_instruction(operation_object)
                        continue

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
                                if isinstance(next_instructions[len(next_instructions) - 1].arg, Label):
                                    raw_else_label = str(by[i - 1].arg).removeprefix(
                                        "<bytecode.instr.Label object at ").removesuffix(">")
                                    next_instructions.remove(next_instructions[len(next_instructions) - 1])
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

                    if len(by) <= i or raw_else_label == "":
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

                case "RETURN_VALUE":
                    previous_instructions = [by[i - 1]]

                    if isinstance(previous_instructions[0], Label):
                        i = i + 1
                        continue
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
                    elif previous_instructions[0].name == "CONTAINS_OP":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("Operation")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "POP_TOP":
                        if by[i - 2].name == "ROT_TWO":
                            copy = by[:i - 2]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            return_object = ReturnObject()
                            return_object.set_argument(return_values[0])
                            return_object.set_type(str(type(return_values[0])))
                            function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "BUILD_CONST_KEY_MAP":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("BuildMap")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "BUILD_TUPLE":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        if len(return_values[0]) == 0:
                            return_object = ReturnObject()
                            return_object.set_type("tuple")
                            function_object.set_return_object(return_object)
                            i = i + 1
                            continue
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("tuple")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "CALL_FUNCTION_KW":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        if len(return_values[0]) == 0:
                            return_object = ReturnObject()
                            return_object.set_type("CallFunction")
                            function_object.set_return_object(return_object)
                            i = i + 1
                            continue
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        if isinstance(return_values[0], str):
                            return_object.set_argument(return_values[0])
                        return_object.set_type("CallFunction")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "BINARY_SUBSCR":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("Operation")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "BINARY_SUBTRACT":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("Operation")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name.__contains__("_OP"):
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("Operation")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "BINARY_MODULO":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("Operation")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "POP_BLOCK":
                        copy = by[:i - 1]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("CallFunction")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "LOAD_DEREF":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("variable")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "BUILD_LIST":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("list")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "BINARY_TRUE_DIVIDE":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("Operation")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "CALL_FUNCTION_EX":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        return_object = ReturnObject()
                        return_object.set_argument(return_values[0])
                        return_object.set_type("CallFunction")
                        function_object.set_return_object(return_object)
                    elif previous_instructions[0].name == "DELETE_FAST":
                        # Skipping...
                        copy = by[:i]
                        copy.reverse()
                        return_object = ReturnObject()
                        return_object.set_type("variable")
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

                # CallMethod -> LOAD_NAME LOAD_ATTR LOAD_METHOD CALL_METHOD
                case "CALL_METHOD":

                    copy = by[:i + 1]
                    copy.reverse()
                    return_values = self.arguments_instructions(copy)

                    # Create a call function object
                    call_function = CallFunctionObject()

                    call_function_reader = CallFunctionReader()
                    call_function_reader.read_call_function(call_function, return_values[0], debug_active)
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

                    if i + 1 != len(by):
                        if isinstance(by[i + 1], Label):
                            i = i + 1
                            continue
                        elif by[i + 1].name != "POP_TOP":
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
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        operation = OperationObject()
                        operation.set_operation_type("in")
                        operation.set_second_operand(return_values[0])
                        if len(return_values[1]) != 0:
                            return_values = self.arguments_instructions(return_values[1])
                            return_values = self.recursive_identification(return_values[0])
                            operation.set_first_operand(return_values[0])
                        variable_condition.set_argument(operation)
                        variable_condition.set_type("Operation")
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
                        variable_condition = VariableObject()
                        variable_condition.set_variable_name(return_values[0])
                    elif previous_instruction[0].name == "LOAD_GLOBAL":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable_condition.set_variable_name(return_values[0])
                    elif previous_instruction[0].name == "LOAD_ATTR":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])

                        variable_condition.set_variable_name(return_values[0])
                        variable_condition.set_type("variable")
                    elif previous_instruction[0].name == "LOAD_DEREF":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])

                        variable_condition.set_variable_name(return_values[0])
                        variable_condition.set_type("variable")
                    elif previous_instruction[0].name == "BUILD_TUPLE":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])

                        variable_condition.set_variable_name(return_values[0])
                        variable_condition.set_type("tuple")
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
                        if i == len(by):
                            break
                        if isinstance(by[i], Label):
                            for_label_esadecimal = str(by[i]).removeprefix(
                                "<bytecode.instr.Label object at ").removesuffix(
                                ">")
                            if for_label_esadecimal == label_esadecimal:
                                break
                            else:
                                body_instructions.append(by[i])
                                i = i + 1
                                if i == len(by):
                                    break

                    # Call a File Reader for read the instructions of body
                    fake_function_object = FunctionObject()
                    self.read_function(fake_function_object, body_instructions, debug_active)

                    for instruction in fake_function_object.get_instructions_list():
                        cicle_object.add_instruction(instruction)

                    if i < len(by):
                        i = i + 1
                        if i < len(by):
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
                        str(variable_name) + "[" + str(square_parenthesis) + "]")

                    if isinstance(previous_instructions[0], Label):
                        i = i + 1
                        continue
                    # Variable -> LOAD_CONST LOAD_NAME LOAD_CONST STORE_SUBSCR
                    elif previous_instructions[0].name == "LOAD_CONST":
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
                        if previous_instructions[1].name == "GET_ITER":
                            variable_object.set_argument(call_function)
                            variable_object.set_type("CallMethod")
                            i = i + 1
                            continue

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
                    elif previous_instructions[0].name == "BINARY_TRUE_DIVIDE":
                        return_values = self.arguments_instructions(previous_instructions)
                        return_values = self.recursive_identification(return_values[0])
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("Operation")
                    elif previous_instructions[0].name == "BINARY_SUBSCR":
                        return_values = self.arguments_instructions(previous_instructions)
                        return_values = self.recursive_identification(return_values[0])
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("Operation")
                    elif previous_instructions[0].name == "BUILD_SLICE":
                        return_values = self.arguments_instructions(previous_instructions)
                        return_values = self.recursive_identification(return_values[0])
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("Operation")
                    elif previous_instructions[0].name == "LOAD_ATTR":
                        return_values = self.arguments_instructions(previous_instructions)
                        return_values = self.recursive_identification(return_values[0])
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("variable")
                    elif previous_instructions[0].name == "BUILD_MAP":
                        return_values = self.arguments_instructions(previous_instructions)
                        return_values = self.recursive_identification(return_values[0])
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("BuildMap")
                    elif previous_instructions[0].name == "LOAD_DEREF":
                        return_values = self.arguments_instructions(previous_instructions)
                        return_values = self.recursive_identification(return_values[0])
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("variable")
                    else:
                        print("STORE_SUBSCR Not registered")
                        print(previous_instructions[0])

                    # Add the variable at instruction list
                    function_object.add_instruction(variable_object)

                case "STORE_ATTR":
                    previous_instructions = [by[i - 1]]

                    # Create a variable object
                    variable = VariableObject()

                    # Variable(Function) -> LOAD_CONST LOAD_FAST STORE_ATTR
                    if previous_instructions[0].name == "LOAD_FAST":
                        previous_instructions.append(by[i - 2])
                        if isinstance(previous_instructions[1], Label):
                            copy = by[:i]
                            copy.reverse()
                            variable.set_type("Boolean")
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> LOAD_CONST STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "LOAD_CONST":
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                            variable.set_argument(previous_instructions[1].arg)
                            variable.set_type(str(type(previous_instructions[1].arg).__name__))
                        # Variable -> CallFunction STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "CALL_FUNCTION":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("CallFunction")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> CallMethod STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "CALL_METHOD":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("CallMethod")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> CallFunction STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "CALL_FUNCTION_KW":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("CallFunction")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> BUILD_LIST STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "BUILD_LIST":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("BuildList")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> BINARY_ADD STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "BINARY_ADD":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("Operation")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> BUILD_CONST_KEY_MAP STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "BUILD_CONST_KEY_MAP":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("BuildMap")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> LOAD_FAST STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "LOAD_FAST":
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)

                            # Create the Variable Object
                            other_variable = VariableObject()
                            other_variable.set_variable_name(previous_instructions[1].arg)
                            other_variable.set_type("variable")
                            # Set the 1* Variable Object at 2* Variable Object
                            variable.set_argument(other_variable)
                        # Variable -> LOAD_ATTR STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "LOAD_ATTR":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("variable")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> LOAD_ATTR STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "UNPACK_SEQUENCE":
                            # Left Part
                            copy = by[i - 2:]
                            number_of_arguments = copy[0].arg
                            counter_copy = 1
                            arguments_counter = 0
                            variable_list = list()
                            while arguments_counter < number_of_arguments:
                                variable_in_list = VariableObject()
                                if copy[counter_copy].name == "LOAD_FAST":
                                    counter_copy = counter_copy + 2
                                    real_copy = copy[:counter_copy]
                                    real_copy.reverse()
                                    return_values = self.arguments_instructions(real_copy)
                                    return_values = self.recursive_identification(return_values[0])
                                    variable_in_list.set_variable_name(return_values[0])
                                    variable_in_list.set_type("variable")
                                else:
                                    print("Not registered UNPACK_SEQUENCE")
                                    print(copy[counter_copy])
                                    exit(-1)
                                variable_list.append(variable_in_list)
                                arguments_counter = arguments_counter + 1

                            save_by = copy[counter_copy:]

                            # Right Part
                            copy = by[:i - 2]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])

                            argument = return_values[0]

                            while len(variable_list) != 0:
                                variable_list[0].set_argument(argument)
                                # Add variabile at variable list of class
                                function_object.add_variable(variable_list[0])
                                variable_list.remove(variable_list[0])

                            by = save_by
                            continue
                        # Variable -> LOAD_GLOBAL STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "LOAD_GLOBAL":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("variable")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> BINARY_TRUE_DIVIDE STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "BINARY_TRUE_DIVIDE":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("variable")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> BUILD_MAP STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "BUILD_MAP":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("variable")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> CallFunction STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "CALL_FUNCTION_EX":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("CallFunction")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> BINARY_SUBSCR STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "BINARY_SUBSCR":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("CallFunction")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        # Variable -> BINARY_MODULO STORE_FAST STORE_ATTR
                        elif previous_instructions[1].name == "BINARY_MODULO":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("Operation")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        elif previous_instructions[1].name == "BINARY_FLOOR_DIVIDE":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("Operation")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        elif previous_instructions[1].name == "BINARY_MULTIPLY":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("Operation")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        elif previous_instructions[1].name == "BINARY_LSHIFT":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("Operation")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        elif previous_instructions[1].name == "LOAD_DEREF":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("variable")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        elif previous_instructions[1].name == "ROT_TWO":
                            # Skipping...
                            variable.set_type("variable")
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        elif previous_instructions[1].name == "STORE_ATTR":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("variable")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        elif previous_instructions[1].name == "BUILD_TUPLE":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("variable")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        elif previous_instructions[1].name == "DICT_UPDATE":
                            copy = by[:i - 1]
                            copy.reverse()
                            return_values = self.arguments_instructions(copy)
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_type("variable")
                            variable.set_argument(return_values[0])
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        elif previous_instructions[1].name == "DUP_TOP":
                            variable.set_type("variable")
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        elif previous_instructions[1].name == "MAKE_FUNCTION":
                            variable.set_type("variable")
                            variable.set_variable_name(previous_instructions[0].arg + "." + instruction.arg)
                        else:
                            print("LOAD_FAST Function Reader not registered")
                            print(previous_instructions[1])
                            exit(-1)
                        # Add variabile at variable list of class
                        function_object.add_variable(variable)
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
                                if count < 0:
                                    break
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
                    elif previous_instructions[0].name == "LOAD_ATTR":
                        copy = by[:i + 1]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)

                        raw_arguments_instructions = return_values[1]

                        return_values = self.recursive_identification(return_values[0])

                        # Create a variable object
                        variable = VariableObject()

                        # Set the variable name
                        variable.set_variable_name(return_values[0])

                        return_values = self.arguments_instructions(raw_arguments_instructions)
                        return_values = self.recursive_identification(return_values[0])

                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "BINARY_SUBSCR":
                        copy = by[:i + 1]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)

                        raw_arguments_instructions = return_values[1]

                        return_values = self.recursive_identification(return_values[0])

                        # Create a variable object
                        variable = VariableObject()

                        # Set the variable name
                        variable.set_variable_name(return_values[0])

                        return_values = self.arguments_instructions(raw_arguments_instructions)
                        return_values = self.recursive_identification(return_values[0])

                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "ROT_TWO":
                        copy = by[:i - 1]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)

                        if return_values is None:
                            i = i + 1
                            continue

                        some_info = return_values[1]

                        return_values = self.recursive_identification(return_values[0])
                        argument = return_values[0]

                        return_values = self.arguments_instructions(some_info)
                        return_values = self.recursive_identification(return_values[0])

                        variable = VariableObject()
                        variable.set_variable_name(return_values[0])
                        variable.set_argument(argument)
                        variable.set_type("Operation")
                        function_object.add_variable(variable)
                    else:
                        print("External STORE_ATTR Not registered")
                        print(previous_instructions[0])

                case "STORE_FAST":
                    previous_instructions = [by[i - 1]]
                    # Bad case for a particular if or for
                    if isinstance(previous_instructions[0], Label):
                        i = i + 1
                        continue
                    # Variable -> LOAD_CONST STORE_FAST
                    elif previous_instructions[0].name == "LOAD_CONST":
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
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        # Create a variable object
                        variable = VariableObject()
                        # The current instruction contains the name of variable
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(return_values[0])
                        variable.set_type("BuildMap")
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

                        if i + 1 < len(by):
                            if not isinstance(by[i + 1], Label):
                                if by[i + 1].name == "CALL_FUNCTION":
                                    i = i + 1
                                    continue
                                elif by[i + 1].name == "LOAD_METHOD":
                                    i = i + 1
                                    continue

                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)

                        # Create a call function object
                        call_function = CallFunctionObject()

                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, return_values[0], debug_active)

                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(call_function)
                        variable.set_type("CallFunction")

                        # Add the call function at instructions of file object
                        function_object.add_instruction(variable)
                    # Variable -> CallFunction STORE_FAST
                    elif previous_instructions[0].name == "CALL_FUNCTION":

                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)

                        # Create a call function object
                        call_function = CallFunctionObject()

                        call_function_reader = CallFunctionReader()
                        call_function_reader.read_call_function(call_function, return_values[0], debug_active)

                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
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

                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable_object.set_argument(return_values[0])
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
                        variable.set_type("Operation")

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
                            arguments = arguments + str(by[i].arg) + ","
                            i = i + 1
                            counter_arguments = counter_arguments + 1

                        variable_object.set_argument(arguments.removesuffix(","))

                        # Add the variable at variable list
                        function_object.add_variable(variable_object)
                    elif previous_instructions[0].name == "LOAD_ATTR":
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
                    elif previous_instructions[0].name == "BINARY_SUBTRACT":
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
                    elif previous_instructions[0].name == "INPLACE_ADD":
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
                    elif previous_instructions[0].name == "BINARY_TRUE_DIVIDE":
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
                    elif previous_instructions[0].name == "BINARY_MULTIPLY":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_type("Operation")

                        # Get the previous instructions
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        # Skipping...
                        if len(return_values[0]) == 1:
                            function_object.add_variable(variable)
                            i = i + 1
                            continue
                        return_values = self.recursive_identification(return_values[0])
                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "UNARY_NEGATIVE":
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
                    elif previous_instructions[0].name == "BUILD_TUPLE":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_type("tuple")

                        # Get the previous instructions
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "CALL_FUNCTION_EX":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_type("CallFunction")

                        # Get the previous instructions
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "BUILD_CONST_KEY_MAP":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_type("BuildMap")

                        # Get the previous instructions
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        if len(return_values[0]) != 0:
                            return_values = self.recursive_identification(return_values[0])
                            variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name.__contains__("_OP"):
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
                    elif previous_instructions[0].name == "POP_TOP":
                        # Do nothing
                        pass
                    elif previous_instructions[0].name == "DUP_TOP":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_type("variable")

                        # Get the previous instructions
                        copy = by[:i - 1]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "STORE_FAST":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_type("BuildMap")

                        # Get the previous instructions
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "BINARY_OR":
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
                    elif previous_instructions[0].name == "BINARY_RSHIFT":
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
                    elif previous_instructions[0].name == "BINARY_FLOOR_DIVIDE":
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
                    elif previous_instructions[0].name == "BINARY_MODULO":
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
                    elif previous_instructions[0].name == "INPLACE_TRUE_DIVIDE":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_type("/= Operation")

                        # Get the previous instructions
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "ROT_TWO":
                        copy = by[:i - 1]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)

                        some_info = return_values[1]

                        return_values = self.recursive_identification(return_values[0])
                        argument = return_values[0]

                        return_values = self.arguments_instructions(some_info)
                        return_values = self.recursive_identification(return_values[0])

                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(argument)
                        variable.set_type("Operation")
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "INPLACE_AND":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_type("And Operation")

                        # Get the previous instructions
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "STORE_DEREF":
                        # Skipping...
                        i = i + 1
                        continue
                    elif previous_instructions[0].name == "INPLACE_SUBTRACT":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_type("-= Operation")

                        # Get the previous instructions
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
                    elif previous_instructions[0].name == "BUILD_SET":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_type("BuildSet")

                        # Get the previous instructions
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        variable.set_argument(return_values[0])
                        function_object.add_variable(variable)
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
            if isinstance(by[counter], Label):
                # Skipping...
                return "Skip", []
            elif by[counter].name == "LOAD_CONST" or by[counter].name == "LOAD_GLOBAL" or by[
                counter].name == "LOAD_NAME" \
                    or by[counter].name == "LOAD_DEREF":
                value = by[counter].arg
                counter = counter + 1
                return value, by[counter:]
            elif by[counter].name == "LOAD_ATTR" or by[counter].name == "STORE_ATTR":
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

                if len(by) == counter:
                    return call_function, []

                return_values = self.recursive_identification(by[counter:])
                call_function.set_method_name(return_values[0])
                by = return_values[1]
                counter = 0
                return call_function, by[counter:]
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

                if len(by) != counter:
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

                if len(by) == counter:
                    return "", []

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
            elif by[counter].name == "BINARY_SUBTRACT":
                counter = counter + 1

                if len(by[counter:]) == 0:
                    return "[" + "]", []

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
            elif by[counter].name == "BINARY_TRUE_DIVIDE":
                counter = counter + 1

                # First Operand
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                division = " / " + str(return_values[0])

                # Second Operand
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                division = str(return_values[0]) + division

                return division, by[counter:]
            elif by[counter].name == "BINARY_MULTIPLY":
                counter = counter + 1

                # First Operand
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                multiply = " * " + str(return_values[0])

                # Second Operand
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                multiply = str(return_values[0]) + multiply

                return multiply, by[counter:]
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
                if len(by[counter:]) != 0:
                    # Second Operand
                    return_values = self.recursive_identification(by[counter:])
                    operation_object.set_second_operand(return_values[0])
                    by = return_values[1]
                    counter = 0
                return operation_object, by[counter:]
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
                    raw_map = raw_map + str(arguments_list[counter_arguments]) + ":" + str(return_values[0]) + ","
                    by = return_values[1]
                    counter = 0
                    counter_arguments = counter_arguments + 1
                raw_map = raw_map.removesuffix(",") + "}"
                return raw_map, by[counter:]
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
            elif by[counter].name == "INPLACE_ADD":
                counter = counter + 1
                return_values = self.recursive_identification(by[counter:])
                value = return_values[0]
                by = return_values[1]
                counter = 0
                return value, by[counter:]
            elif by[counter].name == "INPLACE_AND":
                counter = counter + 1
                return_values = self.recursive_identification(by[counter:])
                value = return_values[0]
                by = return_values[1]
                counter = 0
                return value, by[counter:]
            elif by[counter].name == "INPLACE_TRUE_DIVIDE":
                counter = counter + 1
                return_values = self.recursive_identification(by[counter:])
                value = return_values[0]
                by = return_values[1]
                counter = 0
                return value, by[counter:]
            elif by[counter].name == "INPLACE_SUBTRACT":
                counter = counter + 1
                return_values = self.recursive_identification(by[counter:])
                value = return_values[0]
                by = return_values[1]
                counter = 0
                return value, by[counter:]
            elif by[counter].name == "INPLACE_XOR":
                counter = counter + 1
                return_values = self.recursive_identification(by[counter:])
                value = return_values[0]
                by = return_values[1]
                counter = 0
                return value, by[counter:]
            elif by[counter].name == "INPLACE_MULTIPLY":
                counter = counter + 1
                return_values = self.recursive_identification(by[counter:])
                value = return_values[0]
                by = return_values[1]
                counter = 0
                return value, by[counter:]
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

                # BUILD_LIST Jumping...
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                return arguments, by[counter:]
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
                        or by[counter].name == "LOAD_DEREF" or by[counter].name == "BUILD_TUPLE" \
                        or by[counter].name == "BINARY_ADD" or by[counter].name == "BINARY_SUBSCR":
                    return_values = self.recursive_identification(by[counter:])
                    variable_condition.set_argument(return_values[0])
                    variable_condition.set_type("variable")
                    by = return_values[1]
                    counter = 0
                else:
                    print("GET_ITER Not registered Function Reader")
                    print(by[counter])

                return_values = self.recursive_identification(by[counter:])
                value = return_values[0]
                by = return_values[1]
                counter = 0
                if not isinstance(value, FunctionObject):
                    if value.__contains__("<"):
                        value = value.removeprefix("<")
                        value = value.removesuffix(">")
                    variable_condition.set_type(str(type(value).__name__))
                    variable_condition.set_variable_name(value)
                cicle_object.set_condition(variable_condition)
                return cicle_object, by[counter:]
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
            elif by[counter].name == "LOAD_CLOSURE":
                value = by[counter].arg
                counter = counter + 1
                return value, by[counter:]
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
            elif by[counter].name == "BINARY_XOR":
                counter = counter + 1
                operation_object = OperationObject()
                operation_object.set_operation_type("XOR")
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
            elif by[counter].name == "BINARY_LSHIFT":
                counter = counter + 1
                operation_object = OperationObject()
                operation_object.set_operation_type("SHIFT")
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
            elif by[counter].name == "BINARY_RSHIFT":
                counter = counter + 1
                operation_object = OperationObject()
                operation_object.set_operation_type("SHIFT")
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
                # TODO i don't know when use the arguments
                return return_values[0], by[counter:]
            elif by[counter].name == "ROT_THREE":
                counter = counter + 1
                return "Skip", by[counter:]
            elif by[counter].name == "STORE_FAST":
                value = by[counter].arg
                return value, by[counter:]
            elif by[counter].name == "DICT_UPDATE":
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

                arguments = arguments.removesuffix(",")

                return arguments, by[counter:]
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
            elif by[counter].name == "SET_UPDATE":
                counter = counter + 1

                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0

                return return_values[0], by[counter:]
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
            elif by[counter].name == "ROT_TWO":
                counter = counter + 1
                return_values = self.recursive_identification(by[counter:])
                by = return_values[1]
                counter = 0
                return return_values[0], by[counter:]
            else:
                print("Recursive identification not registered Function Reader")
                print(by[counter])
                exit(-1)
        else:
            if by.name == "LOAD_FAST" or by.name == "LOAD_GLOBAL" or by.name == "LOAD_DEREF" or by.name == "STORE_FAST":
                value = by.arg
                return value, []
            elif by.name == "LOAD_CONST":
                value = by.arg
                return value, []
            else:
                print("Recursive identification not registered Function Reader Single")
                print(by)
                exit(-1)

    # return_values[0] = instruction/instruction list return_values[1] = bytecode modified
    def arguments_instructions(self, by):
        counter = 0
        if isinstance(by[counter], Label):
            instruction_list = list()
            instruction_list.append(by[counter])

            raw_label = str(by[counter]).removeprefix("<bytecode.instr.Label object at ").removesuffix(">")
            counter = counter + 1
            while not isinstance(by[counter], Label):
                instruction_list.append(by[counter])
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
                    instruction_list.append(by[counter])
                    counter = counter + 1
                elif isinstance(by[counter].arg, Label):
                    internal_raw_label = str(by[counter].arg).removeprefix(
                        "<bytecode.instr.Label object at ").removesuffix(">")
                    if internal_raw_label == raw_label:
                        jump_raw_label = str(by[counter - 1].arg).removeprefix(
                            "<bytecode.instr.Label object at ").removesuffix(">")
                        break
                    instruction_list.append(by[counter])
                    counter = counter + 1

            if isinstance(by[counter], Label):
                return [], []

            if by[counter].name == "JUMP_IF_TRUE_OR_POP":
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])
                by = return_values[1]
                counter = 0
            return instruction_list, by[counter:]
        elif by[counter].name == "LOAD_CONST" or by[counter].name == "LOAD_FAST" or by[counter].name == "LOAD_GLOBAL" \
                or by[counter].name == "LOAD_METHOD" or by[counter].name == "STORE_FAST" \
                or by[counter].name == "LOAD_CLOSURE" or by[counter].name == "LOAD_DEREF":
            value = by[counter]
            counter = counter + 1
            return value, by[counter:]
        elif by[counter].name == "DUP_TOP" or by[counter].name == "POP_TOP":
            instruction_list = list()
            counter = counter + 1
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            return instruction_list, by[counter:]
        elif by[counter].name == "LOAD_ATTR" or by[counter].name == "STORE_ATTR":
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
                if len(by) == counter:
                    return [], []
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])

                by = return_values[1]
                counter = 0
                counter_arguments = counter_arguments + 1

            if len(by) != counter:
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
                or by[counter].name == "BINARY_SUBTRACT" or by[counter].name == "BINARY_MULTIPLY" \
                or by[counter].name == "BINARY_TRUE_DIVIDE" or by[counter].name == "BINARY_FLOOR_DIVIDE":
            instruction_list = list()
            instruction_list.append(by[counter])
            counter = counter + 1
            if isinstance(by[counter], Label):
                return instruction_list, by[counter:]
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

            if len(by) == counter:
                return [], []
            # Name of method
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0

            if len(by) != counter:
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
                if len(by) == counter:
                    return [], []
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
        elif by[counter].name == "CALL_FUNCTION_EX":
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

            if isinstance(by[counter], Instr):
                # Bytecode
                instruction_list.append(by[counter].arg)
            else:
                # Bytecode
                instruction_list.append(by[counter])
            counter = counter + 1
            return instruction_list, by[counter:]
        elif by[counter].name == "BUILD_TUPLE":
            instruction_list = list()
            number_of_arguments = by[counter].arg
            instruction_list.append(by[counter])
            counter = counter + 1
            arguments_counter = 0
            while arguments_counter < number_of_arguments:
                if len(by[counter:]) == 0:
                    return [], []
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])
                by = return_values[1]
                counter = 0
                arguments_counter = arguments_counter + 1

            return instruction_list, by[counter:]
        elif by[counter].name == "BUILD_SET":
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
            if len(by[counter:]) != 0:
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
        elif by[counter].name == "BUILD_CONST_KEY_MAP":
            instruction_list = list()
            instruction_list.append(by[counter])
            number_of_arguments = by[counter].arg
            counter = counter + 1
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            counter_arguments = 0
            while counter_arguments < number_of_arguments:
                if len(by) == counter:
                    return [], []
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])
                by = return_values[1]
                counter = 0
                counter_arguments = counter_arguments + 1
            return instruction_list, by[counter:]
        elif by[counter].name == "INPLACE_ADD":
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
        elif by[counter].name == "INPLACE_AND":
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
        elif by[counter].name == "INPLACE_TRUE_DIVIDE":
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
        elif by[counter].name == "INPLACE_SUBTRACT":
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
        elif by[counter].name == "INPLACE_XOR":
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
        elif by[counter].name == "INPLACE_MULTIPLY":
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
        elif by[counter].name == "UNARY_NEGATIVE":
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
        elif by[counter].name == "LIST_EXTEND":
            instruction_list = list()
            number_of_arguments = by[counter].arg
            instruction_list.append(by[counter])
            counter = counter + 1
            counter_arguments = 0
            # Arguments
            while counter_arguments < number_of_arguments:
                return_values = self.arguments_instructions(by[counter:])
                try:
                    instruction_list.extend(return_values[0])
                except TypeError:
                    instruction_list.append(return_values[0])
                by = return_values[1]
                counter = 0
                counter_arguments = counter_arguments + 1

            # BUILD_LIST instruction
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            return instruction_list, by[counter:]
        elif by[counter].name == "BINARY_POWER":
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
        elif by[counter].name == "JUMP_IF_TRUE_OR_POP":
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
        elif by[counter].name == "LIST_TO_TUPLE":
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
        elif by[counter].name == "DICT_MERGE":
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
        elif by[counter].name == "BINARY_AND":
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
        elif by[counter].name == "BINARY_LSHIFT":
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
        elif by[counter].name == "BINARY_RSHIFT":
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
        elif by[counter].name == "BINARY_OR":
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
        elif by[counter].name == "BINARY_XOR":
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
        elif by[counter].name == "BUILD_STRING":
            instruction_list = list()
            instruction_list.append(by[counter])
            number_of_arguments = by[counter].arg
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
        elif by[counter].name == "FORMAT_VALUE":
            instruction_list = list()
            instruction_list.append(by[counter])
            number_of_arguments = by[counter].arg
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

            if len(by) == counter:
                return [], []
            return_values = self.arguments_instructions(by[counter:])
            try:
                instruction_list.extend(return_values[0])
            except TypeError:
                instruction_list.append(return_values[0])
            by = return_values[1]
            counter = 0
            return instruction_list, by[counter:]
        elif by[counter].name == "ROT_THREE":
            instruction_list = list()
            instruction_list.append(by[counter])
            counter = counter + 1
            return instruction_list, by[counter:]
        elif by[counter].name == "LIST_APPEND":
            instruction_list = list()
            instruction_list.append(by[counter])
            number_of_arguments = by[counter].arg
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
        elif by[counter].name == "LOAD_BUILD_CLASS":
            instruction_list = list()
            instruction_list.append(by[counter])
            counter = counter + 1
            return instruction_list, by[counter:]
        elif by[counter].name == "POP_JUMP_IF_FALSE":
            # Skipping...
            return [], []
        elif by[counter].name == "UNPACK_SEQUENCE":
            instruction_list = list()
            instruction_list.append(by[counter])
            number_of_arguments = by[counter].arg
            counter = counter + 1
            counter_arguments = 0
            while counter_arguments < number_of_arguments:
                if len(by) == counter:
                    return [], []
                instruction_list.append(by[counter])
                counter = counter + 1
                counter_arguments = counter_arguments + 1

            return instruction_list, by[counter:]
        elif by[counter].name == "ROT_TWO":
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
        elif by[counter].name == "DICT_UPDATE":
            instruction_list = list()
            instruction_list.append(by[counter])
            number_of_arguments = by[counter].arg
            arguments_counter = 0
            counter = counter + 1
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
        elif by[counter].name == "MAP_ADD":
            instruction_list = list()
            instruction_list.append(by[counter])
            number_of_arguments = by[counter].arg
            arguments_counter = 0
            counter = counter + 1
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
        elif by[counter].name == "SET_UPDATE":
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
        elif by[counter].name == "UNARY_INVERT":
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
        elif by[counter].name == "NOP":
            # Skipping...
            return [], []
        elif by[counter].name == "STORE_DEREF":
            # Skipping...
            return [], []
        elif by[counter].name == "UNARY_NOT":
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
        elif by[counter].name == "GEN_START":
            # Skipping ...
            return [], []
        else:
            print("Arguments instructions not registered")
            print(by[counter])
            exit(-1)
