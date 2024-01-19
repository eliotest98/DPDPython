from Objects.CallFunctionObject import CallFunctionObject
from Objects.VariableObject import VariableObject


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
            if debug_active == 1:
                print(instruction)
            match instruction.name:
                case "STORE_FAST":
                    # If the previous instruction is a LOAD_CONST is a variable.
                    # The variabile have in order:
                    # - LOAD_CONST the value if initialized
                    # - STORE_FAST the name of variable

                    # Get the previous instruction
                    previous_instruction = by[i - 1]
                    if previous_instruction.name == "LOAD_CONST":
                        # Create a Variable Object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(previous_instruction.arg)

                        function_object.add_variable(variable)
                    # self.variable call
                    else:
                        previous_instruction.append(by[i - 2])
                        variable_name = ""
                        for instr in previous_instruction:
                            variable_name = variable_name + instr.arg

                case "LOAD_CONST":
                    # If LOAD_CONST have an arg is a return value
                    # The return value have in order:
                    # - LOAD_CONST
                    # - RETURN_VALUE
                    # There is a possibility to have a self.variable call.
                    # In this case have in order:
                    # - LOAD_FAST | LOAD_CONST
                    # - LOAD_FAST
                    # - STORE_ATTR

                    # Get next instruction
                    next_instruction = by[i + 1]

                    # If the next instruction is a RETURN_VALUE is a return statement
                    if next_instruction.name == "RETURN_VALUE":
                        function_object.set_return_value(instruction.arg)
                        i = i + 1

                    if next_instruction.name == "LOAD_FAST":
                        variable_name = next_instruction.arg + "." + by[i + 2].arg

                        variable = VariableObject()
                        variable.set_variable_name(variable_name)
                        variable.set_argument(by[i].arg)

                        function_object.add_variable(variable)
                        i = i + 2

                case "LOAD_FAST":
                    # Another option for return value is the case of return a variable
                    # The return value with a variable have in order:
                    # - LOAD_FAST
                    # - RETURN_VALUE
                    # There is a possibility to have a call method for return value
                    # In this case have in order:
                    # TODO da controllare se effettivamente c'è questo ordine o ce ne sono anche altri. Sperimentare
                    # - LOAD_FAST
                    # - LOAD_ATTR
                    # - LOAD_METHOD
                    # - CALL_METHOD
                    # - RETURN_VALUE
                    # There is a possibility to have a self.variable call.
                    # In this case have in order:
                    # - LOAD_FAST | LOAD_CONST
                    # - LOAD_FAST
                    # - STORE_ATTR

                    # If the return value is a variable
                    next_instruction = by[i + 1]
                    if next_instruction.name == "RETURN_VALUE":
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        function_object.set_return_value(variable)
                        i = i + 1
                    # Else, the return value is a call function
                    else:

                        # Create a Call Function Object
                        call_function = CallFunctionObject()
                        call_function_path = ""
                        next_instructions = [by[i], by[i + 1], by[i + 2]]

                        # Control if next_instruction is a LOAD_FAST
                        # In this case is a self.variable call
                        if next_instruction.name == "LOAD_FAST":
                            variable_name = next_instruction.arg + "." + by[i + 2].arg

                            variable = VariableObject()
                            variable.set_variable_name(variable_name)
                            variable.set_argument(by[i].arg)

                            function_object.add_variable(variable)
                            i = i + 2
                            continue

                        # Construct the path at method call
                        while len(next_instructions) != 0:
                            if len(next_instructions) == 1:
                                call_function.set_method_name(next_instructions[0].arg)
                            else:
                                call_function_path = call_function_path + next_instructions[0].arg + "."
                            next_instructions.pop(0)
                        call_function.set_path(call_function_path)

                        function_object.set_return_value(call_function)
                        i = i + 2
            i = i + 1

        if debug_active == 1:
            print(function_object.function_name + " End Function Reading\n")
