from bytecode import bytecode

from Objects.CallFunctionObject import CallFunctionObject
from Objects.ClassObject import ClassObject
from Objects.VariableObject import VariableObject
from Readers.ClassReader import ClassReader
from Objects.FunctionObject import FunctionObject
from Readers.FunctionReader import FunctionReader


class FileReader:
    file_directory = ""

    def __init__(self, file_directory):
        self.file_directory = file_directory

    def read_file(self, file_object, bytecode_instructions, debug_active):
        if debug_active == 1:
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
                case "LOAD_BUILD_CLASS":
                    # This token is invoked when create a new class instance
                    # The class instance is formed in order from:
                    # - LOAD_BUILD_CLASS
                    # - LOAD_CONST with object arg (body)
                    # - LOAD_CONST with name of class
                    # - MAKE_FUNCTION
                    # - LOAD_CONST name of making function
                    # - CALL_FUNCTION number of arguments of function
                    # - STORE_NAME name stored
                    next_instruction = by[i + 1]

                    # The next instruction is a LOAD_CONST if is a new class and is an object
                    if next_instruction.name != "LOAD_CONST":
                        break

                    # Create a Class Object
                    internal_class = ClassObject()
                    internal_class.set_class_name("Internal")

                    # Get the bytecode of internal class
                    new_byte = bytecode.Bytecode.from_code(next_instruction.arg)

                    # Start a class reader for read the internal class
                    class_reader = ClassReader()
                    class_reader.read_class(internal_class, new_byte, debug_active)

                    # Add the class at object file
                    file_object.add_class(internal_class)

                    i = i + 6
                case "LOAD_CONST":
                    if instruction.arg is None:
                        i = i + 1
                        continue
                    else:
                        # If a LOAD_CONST is an object is a function
                        # This instruction contains the body of function
                        # The next 3 instruction contains the name of function in order:
                        # - LOAD_CONST
                        # - MAKE_FUNCTION
                        # - STORE_NAME
                        # If a LOAD_CONST is not an object is a variable
                        # This instruction contains the assignment value of variable
                        # The next instruction if is a variable is a STORE_NAME,
                        # The variabile have in order:
                        # - LOAD_CONST the value if initialized
                        # - STORE_NAME the name of variable

                        next_instructions = [by[i + 1], by[i + 2], by[i + 3]]
                        if next_instructions[2].name == "STORE_NAME":
                            function_name = next_instructions[2].arg

                            # Create a Function Object
                            function = FunctionObject()
                            function.set_function_name(function_name)

                            # Get the bytecode of internal function
                            new_byte = bytecode.Bytecode.from_code(instruction.arg)

                            # Start a function reader for read the internal function
                            function_reader = FunctionReader()
                            function_reader.read_function(function, new_byte)

                            # Add function at list of functions of the class
                            file_object.add_function(function)

                            # If the function name is __init__ is a constructor
                            if function_name == "__init__":
                                file_object.set_constructor(function)

                            i = i + 3
                        # Is a variable
                        else:
                            if next_instructions[0].name == "STORE_NAME":
                                # Create a Variable Object
                                variable = VariableObject()
                                variable.set_variable_name(next_instructions[0].arg)
                                variable.set_argument(instruction.arg)

                                file_object.add_variable(variable)
                                i = i + 1

                case "LOAD_NAME":
                    # This instruction is the name of function for call it
                    # The call function is formed in order from:
                    # - LOAD_NAME
                    # - CALL_FUNCTION
                    #
                    # Is possible call a function in a function.
                    # In this case we would have:
                    # - LOAD_NAME
                    # - LOAD_NAME
                    # - CALL_FUNCTION
                    # - CALL_FUNCTION
                    # Another possibility is a variable with a call function
                    # In this case in order have: P.S. There is a four option and is the combination of
                    # previous possibility
                    # - LOAD_NAME | LOAD_NAME * 2
                    # - CALL_FUNCTION | CALL_FUNCTION * 2
                    # - STORE_NAME

                    next_instructions = list()
                    while by[i].name == "LOAD_NAME":
                        next_instructions.append(by[i])
                        i = i + 1

                    prevision = by[i + len(next_instructions)]

                    # Variable Object Temporary
                    variable = VariableObject()
                    var = 0
                    # is a variable with a call function
                    if prevision.name == "STORE_NAME":
                        variable.set_variable_name(prevision.arg)
                        var = 1

                    # is a system call
                    method_name = ""
                    if by[i].name == "LOAD_METHOD":
                        method_name = by[i].arg
                        i = i + 1

                    while len(next_instructions) != 0:
                        # Create a Call Function Object
                        call_function_object = CallFunctionObject()

                        if by[i].name == "CALL_METHOD":
                            i = i + 1
                            continue

                        call_function_object.set_method_name(next_instructions[0].arg)
                        next_instructions.pop(0)
                        if len(next_instructions) != 0:
                            # Create an Internal Call Function if the parameter is a Call Function
                            call_function_object_internal = CallFunctionObject()
                            if method_name == "":
                                call_function_object_internal.set_method_name(next_instructions[0].arg)
                                call_function_object_internal.add_parameter(by[i].arg)
                            else:
                                call_function_object_internal.set_path(next_instructions[0].arg + ".")
                                call_function_object_internal.set_method_name(method_name)
                            call_function_object.add_parameter(call_function_object_internal)
                            # If true is a simple call function
                            if var == 0:
                                file_object.add_instruction(call_function_object)
                            # Else is a variable with a call function
                            else:
                                variable.set_argument(call_function_object)
                                file_object.add_instruction(variable)
                        else:
                            break

                        i = i + 1

            i = i + 1
        if debug_active == 1:
            print(file_object.class_name + " End File Reading\n")
