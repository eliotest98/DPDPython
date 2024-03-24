import collections.abc

from bytecode import bytecode, Label, Instr

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

                case "RETURN_VALUE":
                    i = i + 1
                    if i < len(by):
                        if isinstance(by[i], Label):
                            i = i + 1

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
                    false_file_object = FileObject()

                    self.read_file(false_file_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_file_object.get_instructions_list() + false_file_object.get_imports_list() + false_file_object.get_variables_list():
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
                    false_file_object = FileObject()

                    self.read_file(false_file_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_file_object.get_instructions_list() + false_file_object.get_imports_list() + false_file_object.get_variables_list():
                        exception_object.add_instruction_except(exception_name, element)

                    if i < len(by):
                        if isinstance(by[i], Label):
                            i = i + 1

                    if i < len(by):
                        if by[i].name == "RERAISE":
                            i = i + 1
                            if isinstance(by[i], Label):
                                i = i + 1

                    # Add exception object at instructions of file
                    file_object.add_instruction(exception_object)

                # If -> Operation POP_JUMP_IF_FALSE InstructionList POP_TOP
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
                    false_file_object = FileObject()

                    # Get the objects of instructions
                    self.read_file(false_file_object, next_instructions, debug_active)
                    # Add instructions at list
                    for element in false_file_object.get_instructions_list() + false_file_object.get_imports_list() + false_file_object.get_variables_list():
                        if_object.add_instruction_true(element)

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
                    false_file_object = FileObject()

                    # Get the objects of instructions
                    self.read_file(false_file_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_file_object.get_instructions_list() + false_file_object.get_imports_list() + false_file_object.get_variables_list():
                        if_object.add_instruction_false(element)

                    # Add if at file instructions
                    file_object.add_instruction(if_object)

                # If -> Operation POP_JUMP_IF_FALSE InstructionList POP_TOP
                # InstructionList LOAD_CONST RETURN_VALUE <Label> If
                case "POP_JUMP_IF_FALSE":
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

                    next_instructions = list()
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
                    false_file_object = FileObject()

                    # Get the objects of instructions
                    self.read_file(false_file_object, next_instructions, debug_active)
                    # Add instructions at list
                    for element in false_file_object.get_instructions_list() + false_file_object.get_imports_list() + false_file_object.get_variables_list():
                        if_object.add_instruction_true(element)

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
                    false_file_object = FileObject()

                    # Get the objects of instructions
                    self.read_file(false_file_object, next_instructions, debug_active)

                    # Add instructions at list
                    for element in false_file_object.get_instructions_list() + false_file_object.get_imports_list() + false_file_object.get_variables_list():
                        if_object.add_instruction_false(element)

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

                        # Create a call function object for condtion
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
                    elif previous_instruction[0].name == "LOAD_NAME":
                        variable = VariableObject()
                        variable.set_type("variable")
                        variable.set_variable_name(previous_instruction[0].arg)
                        variable_condition.set_argument(variable)
                    else:
                        print("Condition not registered File Reader")
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
                    fake_file_object = FileObject()
                    self.read_file(fake_file_object, body_instructions, debug_active)

                    for instruction in fake_file_object.get_instructions_list():
                        cicle_object.add_instruction(instruction)

                    i = i + 1
                    if isinstance(by[i], Label):
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

                # Variable -> LOAD_CONST LOAD_NAME LOAD_CONST STORE_SUBSCR
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
                        variable_name + "[" + square_parenthesis + "]")

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
                    elif previous_instructions[0].name == "BINARY_SUBTRACT":
                        return_values = self.arguments_instructions(previous_instructions)
                        return_values = self.recursive_identification(return_values[0])
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("CallFunction")
                    elif previous_instructions[0].name == "LOAD_ATTR":
                        return_values = self.arguments_instructions(previous_instructions)
                        return_values = self.recursive_identification(return_values[0])
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("CallFunction")
                    elif previous_instructions[0].name == "BINARY_SUBSCR":
                        return_values = self.arguments_instructions(previous_instructions)
                        return_values = self.recursive_identification(return_values[0])
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("variable")
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
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(copy)
                        if isinstance(return_values[0], FunctionObject):
                            file_object.add_function(return_values[0])
                        else:
                            print("Not registered for the moment")
                            print(return_values[0].abstract_syntax_tree(0))
                            exit(-1)
                        # In this other case is a call function
                        # if previous_instruction[1].name == "GET_ITER":
                        #     # Create a call function object
                        #     call_function = CallFunctionObject()
                        #     call_function_reader = CallFunctionReader()
                        #     call_function_reader.read_call_function(call_function, previous_instruction, debug_active)
                        #
                        #     # Create a variable object
                        #     variable = VariableObject()
                        #     variable.set_variable_name(instruction.arg)
                        #     variable.set_argument(call_function)
                        #     variable.set_type("CallFunction")
                        #
                        #     # Add the call function at instructions of file object
                        #     file_object.add_instruction(variable)
                        #
                        #     i = i + 1
                        # else:
                        #     # Create a class object
                        #     class_object = ClassObject()
                        #     class_object.set_class_name(instruction.arg)
                        #     class_object.set_file_name(file_object.get_class_name())
                        #
                        #     # SuperclassList -> LOAD_NAME -> SuperclassList |
                        #     #                   LOAD_NAME                   |
                        #     #                   /* empty */
                        #     for instruction_part in previous_instruction:
                        #         if instruction_part.name == "LOAD_NAME":
                        #             class_object.add_superclass(instruction_part.arg)
                        #         elif instruction_part.name == "LOAD_CONST" and instruction_part.arg == instruction.arg:
                        #             break
                        #
                        #     # Get the bytecode of internal function
                        #     new_byte = bytecode.Bytecode.from_code(
                        #         previous_instruction[len(previous_instruction) - 2].arg)
                        #
                        #     # remove the first 4 instructions
                        #     # BodyClass -> LOAD_NAME STORE_NAME LOAD_CONST STORE_NAME
                        #     new_byte.pop(0)
                        #     new_byte.pop(0)
                        #     new_byte.pop(0)
                        #     new_byte.pop(0)
                        #
                        #     # Start a class reader for read the body of class
                        #     class_reader = ClassReader()
                        #     class_reader.read_class(class_object, new_byte, debug_active)
                        #
                        #     # Add the class at file object
                        #     file_object.add_class(class_object)
                        #     # Add the class at the system
                        #     self.system_object.add_class(class_object)
                    elif previous_instruction[0].name == "CALL_FUNCTION_KW":
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
                        file_object.add_instruction(variable)
                    # Variable -> CallMethod STORE_NAME
                    elif previous_instruction[0].name == "CALL_METHOD":
                        number_of_line = previous_instruction[0].lineno
                        previous_instruction = list()
                        count = i - 1
                        while by[count].lineno == number_of_line:
                            previous_instruction.append(by[count])
                            count = count - 1
                            if count < 0:
                                break

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

                        # if there is a Label is a Function
                        if isinstance(previous_instruction[0], Label):
                            # Get the bytecode of internal function
                            new_byte = bytecode.Bytecode.from_code(previous_instruction[1].arg)
                            # Start a function reader for read the internal function
                            function_reader = FunctionReader()
                            function_reader.read_function(function, new_byte, debug_active)
                        # Function -> LOAD_CONST Function
                        elif previous_instruction[0].name == "LOAD_CONST":
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
                    elif previous_instruction[0].name == "BINARY_SUBSCR":
                        # Get all the previous instructions
                        copy = by[:i]
                        # Reverse of array
                        copy.reverse()
                        # Get the exactly instructions
                        return_values = self.arguments_instructions(copy)
                        # Get the results from the exactly instructions
                        return_values = self.recursive_identification(return_values[0])
                        # Create a variable object
                        variable_object = VariableObject()
                        variable_object.set_variable_name(instruction.arg)
                        # Set the result of the recursive identification
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("BinarySubscr")
                        file_object.add_variable(variable_object)
                    elif previous_instruction[0].name == "BUILD_LIST":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        # Create a variable object
                        variable_object = VariableObject()
                        variable_object.set_variable_name(instruction.arg)
                        # Set the result of the recursive identification
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("BuildList")
                        file_object.add_variable(variable_object)
                    elif previous_instruction[0].name == "BUILD_CONST_KEY_MAP":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        # Create a variable object
                        variable_object = VariableObject()
                        variable_object.set_variable_name(instruction.arg)
                        # Set the result of the recursive identification
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("BuildMap")
                        file_object.add_variable(variable_object)
                    elif previous_instruction[0].name == "BINARY_ADD":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        # Create a variable object
                        variable_object = VariableObject()
                        variable_object.set_variable_name(instruction.arg)
                        # Set the result of the recursive identification
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("Operation")
                        file_object.add_variable(variable_object)
                    elif previous_instruction[0].name == "UNPACK_SEQUENCE":
                        # Create a Variable Object
                        variable_object = VariableObject()
                        variable_object.set_variable_name(instruction.arg)
                        variable_object.set_type("VariableSequence")
                        arguments = ""
                        number_of_arguments = previous_instruction[0].arg
                        counter_arguments = 0
                        while counter_arguments < number_of_arguments:
                            arguments = arguments + by[i].arg + ","
                            i = i + 1
                            counter_arguments = counter_arguments + 1

                        variable_object.set_argument(arguments.removesuffix(","))

                        # Add the variable at variable list
                        file_object.add_variable(variable_object)
                    elif previous_instruction[0].name == "LOAD_ATTR":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        # Create a variable object
                        variable_object = VariableObject()
                        variable_object.set_variable_name(instruction.arg)
                        # Set the result of the recursive identification
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("Operation")
                        file_object.add_variable(variable_object)
                    elif previous_instruction[0].name == "INPLACE_ADD":
                        copy = by[:i]
                        copy.reverse()
                        return_values = self.arguments_instructions(copy)
                        return_values = self.recursive_identification(return_values[0])
                        # Create a variable object
                        variable_object = VariableObject()
                        variable_object.set_variable_name(instruction.arg)
                        # Set the result of the recursive identification
                        variable_object.set_argument(return_values[0])
                        variable_object.set_type("Operation +=")
                        file_object.add_variable(variable_object)
                    else:
                        print("STORE_NAME not registered File Reader")
                        print(previous_instruction[0])

            i = i + 1
        if debug_active == 1:
            if isinstance(file_object, CicleObject):
                print("Cicle Body End Reading\n")
            else:
                print(file_object.class_name + " End File Reading\n")

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
            elif by[counter].name == "LOAD_METHOD":
                value = by[counter].arg
                counter = counter + 1
                return value, by[counter:]
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
            elif by[counter].name == "INPLACE_ADD":
                counter = counter + 1
                return_values = self.recursive_identification(by[counter:])
                value = return_values[0]
                by = return_values[1]
                counter = 0
                return value, by[counter:]
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
                function_reader = FunctionReader()
                function_reader.read_function(function_object, internal_bytecode, 0)
                counter = counter + 1
                return function_object, by[counter:]
            else:
                print("Recursive identification not registered File Reader")
                print(by[counter])
                exit(-1)
        else:
            if by.name == "LOAD_FAST":
                value = by.arg
                variable = VariableObject()
                variable.set_variable_name(value)
                variable.set_type("variable")
                return variable, []
            elif by.name == "LOAD_CONST":
                value = by.arg
                variable = VariableObject()
                variable.set_variable_name(value)
                variable.set_type("variable")
                return variable, []
            elif by.name == "LOAD_NAME":
                value = by.arg
                variable = VariableObject()
                variable.set_variable_name(value)
                variable.set_type("variable")
                return variable, []
            else:
                print("Recursive identification not registered File Reader Single")
                print(by)
                exit(-1)

    # return_values[0] = instruction/instruction list return_values[1] = bytecode modified
    def arguments_instructions(self, by):
        counter = 0
        if by[counter].name == "LOAD_CONST" or by[counter].name == "LOAD_FAST" or by[counter].name == "LOAD_GLOBAL" \
                or by[counter].name == "LOAD_METHOD" or by[counter].name == "STORE_FAST" \
                or by[counter].name == "LOAD_NAME":
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
                or by[counter].name == "BINARY_SUBTRACT" or by[counter].name == "BINARY_AND":
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
        else:
            print("Arguments instructions not registered File Reader")
            print(by[counter])
            exit(-1)
