from Objects.FileObject import FileObject
from Objects.FunctionObject import FunctionObject
from Objects.ReturnObject import ReturnObject
from Objects.VariableObject import VariableObject


class ConstructorDetector:

    def __init__(self, system_object):
        self.create_constructors(system_object)

    # This method create the constructors if not exist
    def create_constructors(self, system_object):
        for i in range(system_object.get_class_number()):
            class_object = system_object.get_class_object_with_position(i)
            if not isinstance(class_object, FileObject):
                if class_object.get_constructor().get_function_name() != "":
                    # Get the constructor
                    constructor = class_object.get_constructor()
                    for superclass in class_object.get_superclass_list():
                        superclass_name = superclass
                        if superclass.__contains__("Import:"):
                            superclass_name = superclass.removeprefix("Import:")
                        self_variable = VariableObject()
                        self_variable.set_type(superclass_name)
                        self_variable.set_variable_name("self." + superclass_name.lower())
                        internal_variable = VariableObject()
                        internal_variable.set_variable_name(superclass_name.lower())
                        internal_variable.set_type("variable")
                        self_variable.set_argument(internal_variable)
                        constructor.add_variable(self_variable)
                    class_object.set_constructor(constructor)
                else:
                    # Create the constructor
                    constructor = FunctionObject()
                    # Set a name at constructor
                    constructor.set_function_name("__init__")

                    # Create a fake Return Object
                    return_object = ReturnObject()
                    return_object.set_type("NoneType")
                    return_object.set_argument("None")
                    constructor.set_return_object(return_object)

                    for superclass in class_object.get_superclass_list():
                        superclass_name = superclass
                        if superclass.__contains__("Import:"):
                            superclass_name = superclass.removeprefix("Import:")
                        self_variable = VariableObject()
                        self_variable.set_type(superclass_name)
                        self_variable.set_variable_name("self." + superclass_name.lower())
                        internal_variable = VariableObject()
                        internal_variable.set_variable_name(superclass_name.lower())
                        internal_variable.set_type("variable")
                        self_variable.set_argument(internal_variable)
                        constructor.add_variable(self_variable)

                    # Set the constructor and add in the function list
                    class_object.set_constructor(constructor)
                    class_object.add_function(constructor)
