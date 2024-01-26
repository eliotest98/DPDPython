from bytecode import Label

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
            if isinstance(instruction, Label):
                i = i + 1
                continue
            if debug_active == 1:
                print(instruction)
            match instruction.name:

                case "POP_JUMP_IF_TRUE":
                    # This instruction is an if statement
                    # An if statement is formed in order from:
                    # - instructions for comparison
                    # - POP_JUMP_IF_TRUE
                    # - instructions
                    # - JUMP_FORWARD
                    # - Label jump
                    while not isinstance(by[i], Label):
                        if by[i].name == "JUMP_FORWARD":
                            i = i + 1
                        i = i + 1
                    function_object.add_instruction("<IF>If Statement</IF>")

                case "FOR_ITER":
                    # If the previous instruction is a FOR_ITER is a cicle.
                    # The variabile have in order:
                    # - FOR_ITER the value if initialized
                    # - instructions
                    # - JUMP_ABSOLUTE
                    function_object.add_instruction("Iteration")
                    while by[i].name != "JUMP_ABSOLUTE":
                        i = i + 1
                        if isinstance(by[i], Label):
                            i = i + 1

                case "LOAD_GLOBAL":
                    # This instruction is the name of function for call it
                    # The call function is formed in order from:
                    # - LOAD_GLOBAL
                    # - LOAD_CONST
                    # - CALL_FUNCTION
                    next_instructions = [by[i + 1], by[i + 2]]
                    if next_instructions[1].name == "CALL_FUNCTION":
                        if next_instructions[0].name == "LOAD_CONST":
                            # Create a Call Function Object
                            call_function = CallFunctionObject()
                            call_function.set_method_name(instruction.arg)
                            call_function.add_parameter(next_instructions[0].arg)

                            # Add instruction at function
                            function_object.add_instruction(call_function)
                            i = i + 2

                    # There is another method for call a function:
                    # - LOAD_GLOBAL
                    # - LOAD_METHOD
                    # - CALL_METHOD
                    # There is another method for call a function:
                    # - LOAD_GLOBAL
                    # - LOAD_METHOD
                    # - LOAD_FAST
                    # - CALL_METHOD
                    # There is another method for call a function:
                    # - LOAD_GLOBAL
                    # - LOAD_METHOD *
                    # - LOAD_FAST *
                    # - CALL_METHOD *
                    if next_instructions[0].name == "LOAD_METHOD":

                        # Create a Call Function Object
                        call_function = CallFunctionObject()

                        count = i + 1
                        path = instruction.arg + "."
                        while by[count].name == "LOAD_METHOD":
                            next_instructions = [by[i + 4], by[i + 5], by[i + 6]]
                            if next_instructions[0].name != "LOAD_METHOD":
                                call_function.add_parameter(by[count + 1].arg)
                                path = path + by[count].arg
                            else:
                                path = path + by[count].arg + "(" + str(by[count + 1].arg) + ")."
                            count = count + 3
                            i = i + 3

                        path = path.removesuffix(".")
                        call_function.set_method_name(path)

                        # Add instruction at function
                        function_object.add_instruction(call_function)

                        '''
                        if next_instructions[1].name == "LOAD_FAST":
                            # Create a Call Function Object
                            call_function = CallFunctionObject()
                            call_function.set_method_name(next_instructions[0].arg)
                            call_function.set_path(instruction.arg + ".")
                            call_function.add_parameter(next_instructions[1].arg)

                            # Add instruction at function
                            function_object.add_instruction(call_function)
                            i = i + 3
                        else:
                            # Create a Call Function Object
                            call_function = CallFunctionObject()
                            call_function.set_method_name(next_instructions[0].arg)
                            call_function.set_path(instruction.arg + ".")

                            # Add instruction at function
                            function_object.add_instruction(call_function)
                            i = i + 2
                        '''

                case "STORE_FAST":

                    # Get the previous instruction
                    previous_instruction = by[i - 1]

                    # If the previous instruction is a LOAD_CONST is a variable.
                    # The variabile have in order:
                    # - LOAD_CONST the value if initialized
                    # - STORE_FAST the name of variable
                    if previous_instruction.name == "LOAD_CONST":
                        # Create a Variable Object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)
                        variable.set_argument(previous_instruction.arg)
                        function_object.add_variable(variable)
                        i = i + 1
                        continue

                    # If the previous instruction is a CALL_FUNCTION_KW is a variable with a call function.
                    # The variabile have in order:
                    # - LOAD_CONST the value if initialized
                    # - CALL_FUNCTION_KW
                    if previous_instruction.name == "CALL_FUNCTION_KW":
                        # Create a Variable Object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)

                        # TODO da vedere
                        variable.set_argument(CallFunctionObject())

                        function_object.add_variable(variable)
                        i = i + 1
                        continue

                    # If the previous instruction is a CALL_METHOD is a variable with a call function.
                    # The variabile have in order:
                    # - LOAD_CONST the value if initialized
                    # - CALL_METHOD
                    if previous_instruction.name == "CALL_METHOD":
                        # Create a Variable Object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)

                        # TODO da vedere
                        variable.set_argument(CallFunctionObject())

                        function_object.add_variable(variable)
                    # self.variable call
                    else:
                        previous_instruction = [by[i - 1], by[i - 2]]
                        variable_name = ""
                        for instr in previous_instruction:
                            if isinstance(instr.arg, int):
                                variable_name = variable_name + str(instr)
                            else:
                                variable_name = variable_name + instr.arg

                case "LOAD_CONST":

                    # Get next instruction
                    next_instruction = by[i + 1]

                    # If LOAD_CONST have an arg is a return value
                    # The return value have in order:
                    # - LOAD_CONST
                    # - RETURN_VALUE
                    if next_instruction.name == "RETURN_VALUE":
                        function_object.set_return_value(instruction.arg)
                        i = i + 1

                    # There is a possibility to have a self.variable call.
                    # In this case have in order:
                    # - LOAD_FAST | LOAD_CONST
                    # - LOAD_FAST
                    # - STORE_ATTR
                    if next_instruction.name == "LOAD_FAST":
                        variable_name = next_instruction.arg + "." + by[i + 2].arg

                        variable = VariableObject()
                        variable.set_variable_name(variable_name)
                        variable.set_argument(by[i].arg)

                        function_object.add_variable(variable)
                        i = i + 2

                case "LOAD_FAST":

                    # An option for return value is the case of return a variable
                    # The return value with a variable have in order:
                    # - LOAD_FAST
                    # - RETURN_VALUE
                    next_instruction = by[i + 1]
                    if next_instruction.name == "RETURN_VALUE":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(instruction.arg)

                        # Add the return value at function
                        function_object.set_return_value(variable)
                        i = i + 1
                        continue

                    # There is a possibility to have a foreach for return value
                    # In this case have in order:
                    # - LOAD_FAST
                    # - GET_ITER
                    # - CALL_FUNCTION
                    # - RETURN_VALUE
                    if next_instruction.name == "GET_ITER":
                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name("Iteration")

                        # Add the return value at function
                        function_object.set_return_value(variable)
                        i = i + 3
                        continue

                    # There is a possibility to have a self.variable call.
                    # In this case have in order:
                    # - LOAD_FAST | LOAD_CONST
                    # - LOAD_FAST
                    # - STORE_ATTR
                    if next_instruction.name == "LOAD_FAST":
                        variable_name = next_instruction.arg + "." + by[i + 2].arg

                        # Create a variable object
                        variable = VariableObject()
                        variable.set_variable_name(variable_name)
                        variable.set_argument(by[i].arg)

                        function_object.add_variable(variable)
                        i = i + 3
                        continue

                    # There is a possibility to have a call method for return value
                    # In this case have in order:
                    # - LOAD_FAST
                    # - LOAD_ATTR
                    # - LOAD_METHOD
                    # - CALL_METHOD
                    # - RETURN_VALUE
                    if next_instruction.name == "LOAD_ATTR":
                        # Create a Call Function Object
                        call_function = CallFunctionObject()
                        call_function_path = ""
                        next_instructions = [by[i], by[i + 1], by[i + 2]]
                        if by[i + 4].name == "RETURN_VALUE":
                            while len(next_instructions) != 0:
                                if len(next_instructions) == 1:
                                    call_function.set_method_name(next_instructions[0].arg)
                                else:
                                    call_function_path = call_function_path + next_instructions[0].arg + "."
                                next_instructions.pop(0)
                            call_function.set_path(call_function_path)

                            function_object.set_return_value(call_function)
                            i = i + 2
                        continue

                    # Another possibility is a nested call function for return value
                    # In this case have in order:
                    # - LOAD_FAST
                    # - others instructions
                    # - CALL_METHOD
                    # - RETURN_VALUE
                    while by[i].name != "RETURN_VALUE":
                        i = i + 1
                        if isinstance(by[i], Label):
                            i = i + 1
                            continue
                    if by[i - 1].name == "CALL_FUNCTION" or by[i - 1].name == "CALL_METHOD":
                        function_object.set_return_value(CallFunctionObject())
                    else:
                        i = i - 2

            i = i + 1

        if debug_active == 1:
            print(function_object.function_name + " End Function Reading\n")
