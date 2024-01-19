from bytecode import bytecode

from Objects.FunctionObject import FunctionObject
from Objects.VariableObject import VariableObject
from Readers.FunctionReader import FunctionReader


class ClassReader:

    def read_class(self, class_object, bytecode_instructions, debug_active):
        if debug_active == 1:
            print("\n" + class_object.class_name + " Class Reading...")
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
                case "LOAD_NAME":
                    # LOAD_NAME is the first token invoked when create a class.
                    # A class is form with 4 informations in order:
                    # - LOAD_NAME for __name__ function
                    # - STORE_NAME for __module__ function
                    # - LOAD_CONST for the name of class
                    # - STORE_NAME for __qualname__ function
                    next_instructions = [by[i + 1], by[i + 2], by[i + 3]]

                    # The second instruction is a LOAD_CONST if is a new class
                    if next_instructions[1].name != "LOAD_CONST":
                        break
                    class_name = next_instructions[1].arg

                    # Set the class name
                    class_object.set_class_name(class_name)

                    i = i + 3

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
                            function_reader.read_function(function, new_byte, debug_active)

                            # Add function at list of functions of the class
                            class_object.add_function(function)

                            # If the function name is __init__ is a constructor
                            if function_name == "__init__":
                                class_object.set_constructor(function)

                            i = i + 3
                        # Is a variable
                        else:
                            if next_instructions[0].name == "STORE_NAME":
                                # Create a Variable Object
                                variable = VariableObject()
                                variable.set_variable_name(next_instructions[0].arg)
                                variable.set_argument(instruction.arg)

                                class_object.add_variable(variable)

                                i = i + 1

            i = i + 1
        if debug_active == 1:
            print(class_object.class_name + " End Class Reading\n")
