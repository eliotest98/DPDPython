import marshal
import os

from bytecode import bytecode

from Objects.FileObject import FileObject
from Readers.FileReader import FileReader


class ReadBytecode:
    # Get the resource directory
    resource_directory = os.getcwd().replace("\\Core", "").replace("\\python", "") + "\\resources"
    debug_active = 1

    def __init__(self):
        if self.debug_active == 1:
            print("Reading Bytecode...")

    def select_file(self, current_directory):
        if os.path.isdir(current_directory):
            for directory in os.listdir(current_directory):
                if os.path.isdir(current_directory + "\\" + directory):
                    self.select_file(current_directory + "\\" + directory)
                else:
                    if directory.__contains__(".pyc"):
                        self.select_file(current_directory + "\\" + directory)
        else:
            if os.path.isfile(current_directory):
                self.read_bytecode(current_directory)
            else:
                # TODO Da vedere se gestire un eccezione
                print("error")

    def visualize_bytecode(self, bytecode_copy):
        print("\nAnalyzing...")
        for instruction in bytecode_copy:
            try:
                by = bytecode.Bytecode.from_code(instruction.arg)
                self.visualize_bytecode(by)
            except:
                print(instruction)
                pass
        print("End Analyzing...\n")

    def read_bytecode(self, file_directory):
        # Open the binary generated
        with open(file_directory, 'rb') as f:
            # TODO Salta l'intestazione del file .pyc ATTENZIONE dipende dalla versione di python (Attuale 3.10)
            f.read(16)
            code_obj = marshal.load(f)

        # Get the bytecode
        by = bytecode.Bytecode.from_code(code_obj)

        if self.debug_active == 1:
            self.visualize_bytecode(by.copy())

        directory_split = code_obj.co_filename.split("\\")
        file_name = directory_split[len(directory_split) - 1]

        if self.debug_active == 1:
            print(file_name + " File Reading...")

        file_reader = FileReader(file_directory)
        file_object = FileObject()
        file_object.set_class_name(file_name.replace(".py", ""))
        file_reader.read_file(file_object, by, self.debug_active)

        if self.debug_active == 1:
            print(file_name + " End File Reading...")

        if self.debug_active == 1:
            # Raw AST
            print(file_object.to_string())

        ast = file_object.abstract_syntax_tree()
        if self.debug_active == 1:
            print("Abstract Syntax Tree")
            print(ast)
        with open(self.resource_directory + "\\AST.xml", "w") as f:
            f.write(ast)
