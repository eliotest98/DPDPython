import os

from Compiler import Compiler
from Core.ReadBytecode import ReadBytecode
from Core.SystemGenerator import SystemGenerator
from Descriptors.AdapterPattern import AdapterPatternDescriptor
from Descriptors.MatrixContainer import MatrixContainer
from Detector.DesignPatternDetection import DesignPatternDetection
from Detector.SuperclassDetector import SuperclassDetector
from Downloader.GithubRepository import GithubRepository

current_directory = os.getcwd().replace("\\Core", "")
# Get the resource directory
resource_directory = current_directory.replace("\\python", "") + "\\resources"
# Get the selected directory
selected_directory = os.getcwd().replace("\\Core", "")

# Compile Oracle Files because there isn't invoked from any class
Compiler.compile_file(current_directory + "\\Oracle\\Adapter\\AdapterPattern.py")
Compiler.compile_file(current_directory + "\\Oracle\\Classes\\Classes.py")
Compiler.compile_file(current_directory + "\\Oracle\\Prova\\__init__.py")

bytecode = ReadBytecode()
# Generate the Oracles Files
bytecode.select_file(current_directory + "\\Oracle\\Adapter", resource_directory + "\\Oracles\\Adapter", 0)
# SuperclassDetector for Oracles Files
SuperclassDetector(bytecode.get_system_object())
# Write on a file the Abstract Syntax Tree (TypeChecked)
with open(resource_directory + "\\Oracles\\SystemObject.xml", "w") as f:
    f.write(bytecode.get_system_object().abstract_syntax_tree())
# System Generator for Oracles Files
system_generator = SystemGenerator(bytecode.get_system_object())

# Download the file from a repository
repository = GithubRepository("AaronWard/covidify", resource_directory + "\\GeneratedFiles\\DirectorySelected")
# repository.download_repository()
# repository.change_permissions()
# repository.delete_files_unused()
# repository.compile_repository_files()
'''bytecode.select_file(resource_directory + "\\GeneratedFiles\\DirectorySelected\\" + "AaronWard\\covidify"
                     + "\\Source"
                     ,
                     resource_directory + "\\GeneratedFiles\\Oracles\\" + "AaronWard\\covidify" + "\\AbstractSyntaxTree",
                     1)'''
# repository.delete_reporitory()

detection = DesignPatternDetection()
detection.set_design_pattern()
detection.generate_results()
