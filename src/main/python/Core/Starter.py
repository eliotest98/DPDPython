import os

import pandas as pd

from Compiler import Compiler
from Core.ReadBytecode import ReadBytecode
from Core.SystemGenerator.Objects.PatternResult import PatternResult
from Core.SystemGenerator.SystemGenerator import SystemGenerator
from Detector.DesignPatternDetector import DesignPatternDetection
from Detector.MethodOriginDetector import MethodOriginDetector
from Detector.SuperclassDetector import SuperclassDetector
from Detector.TypeDetector import TypeDetector
from Detector.VariableDetector import VariableDetector
from Downloader.GithubRepository import GithubRepository
from Utils.DesignPattern import DesignPattern

current_directory = os.getcwd().replace("\\Core", "")
# Get the resource directory
resource_directory = current_directory.replace("\\python", "") + "\\resources"
# Get the selected directory
selected_directory = os.getcwd().replace("\\Core", "")

# Compile Oracle Files because there isn't invoked from any class
Compiler.compile_file(current_directory + "\\Oracle\\Adapter\\AdapterPattern.py")
Compiler.compile_repository_files(current_directory + "\\Oracle\\AdapterExtended")
Compiler.compile_file(current_directory + "\\Oracle\\Classes\\Classes.py")
Compiler.compile_file(current_directory + "\\Oracle\\Test\\__init__.py")

def execute(repository_owner, repository_name, branch_name):
    bytecode = ReadBytecode(debug_active=0)
    # Download the file from a repository
    repository = GithubRepository(repository_owner + "/" + repository_name,
                                  resource_directory + "\\GeneratedFiles\\DirectorySelected", branch_name)
    repository.download_repository()
    repository.change_permissions()
    repository.delete_files_unused()
    repository.compile_repository_files()
    bytecode.select_file(
        resource_directory + "\\GeneratedFiles\\DirectorySelected\\" + repository_owner + "\\" + repository_name + "\\" + "\\Source",
        resource_directory + "\\GeneratedFiles\\Oracles\\" + repository_owner + "\\" + repository_name)
    # repository.delete_reporitory()
    # bytecode.select_file(current_directory + "\\Oracle\\Adapter", resource_directory + "\\Oracles\\Adapter")
    #
    # Detectors
    #
    SuperclassDetector(bytecode.get_system_object())
    VariableDetector(bytecode.get_system_object())
    MethodOriginDetector(bytecode.get_system_object())
    TypeDetector(bytecode.get_system_object())

    # Write on a file the Abstract Syntax Tree (TypeChecked)
    with open(resource_directory + "\\GeneratedFiles\\Oracles\\" +
              repository_owner + "\\SystemObject.xml", "w") as f:
        f.write(bytecode.get_system_object().abstract_syntax_tree())

    #
    # Design Pattern Detection
    #
    detection = DesignPatternDetection()
    # Get informations from system object
    system_generator = SystemGenerator(bytecode.get_system_object())
    # Get hierarchy list of system analized
    hierarchy_list = system_generator.get_hierarchy_list()
    pattern_results = list()
    # Get the list of Design Patterns
    pattern_list = list(DesignPattern)
    for pattern in pattern_list:
        pattern_name = pattern.name
        pattern_result = PatternResult(pattern_name)
        # For now there is only one descriptor
        pattern_descriptor = detection.set_design_pattern(pattern_name)
        # TODO da vedere in quanto dipende dalle gerarchie che in python sono multi
        if pattern_descriptor.get_number_of_hierarchies() == 2:
            # Create the cluster set from system generator with pattern selected
            cluster_set = sorted(system_generator.generate_cluster_set(pattern_descriptor).get_cluster_set())
            for entry in cluster_set:
                # Get the hierarchies
                hierarchies_matrix_container = system_generator.get_hierarchies_matrix_container(
                    entry.get_hierarchy_list())
                # Construct the association matrix
                pattern_descriptor.set_association_matrix(
                    pd.DataFrame(pattern_descriptor.get_association_matrix().values,
                                 index=hierarchies_matrix_container.get_association_matrix().index,
                                 columns=hierarchies_matrix_container.get_association_matrix().columns))
                # Detect of design pattern selected
                detection.generate_results(hierarchies_matrix_container, pattern_descriptor, pattern_result)
        pattern_results.append(pattern_result)

    #
    # Results
    #
    for pattern_individuated in pattern_results:
        print("\nInstance of: " + pattern_individuated.get_pattern_name())
        for pattern_instance in pattern_individuated.get_pattern_instances():
            print("Number of instances: ", pattern_instance.get_instance_counter())
            print(pattern_instance)
        print("----------------------------------------")


#execute("AaronWard", "covidify", "")
execute("chensteven", "covidify", "project-structural-pattern")
