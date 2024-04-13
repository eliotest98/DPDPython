import os
from multiprocessing import Pool

import pandas as pd

from Compiler import Compiler
from Core.ReadBytecode import ReadBytecode
from Core.SystemGenerator.Objects.PatternResult import PatternResult
from Core.SystemGenerator.SystemGenerator import SystemGenerator
from Detector.ConstructorDetector import ConstructorDetector
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


def execute(repository_owner, repository_name, branch_name, debug_active):
    string_to_return = ""

    bytecode = ReadBytecode(debug_active)
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
    repository.delete_repository()

    try:
        # Write on a file the Abstract Syntax Tree of all system
        with open(resource_directory + "\\GeneratedFiles\\Oracles\\" +
                  repository_owner + "\\SystemObject.xml", "w", encoding='utf-8') as f:
            f.write(bytecode.get_system_object().abstract_syntax_tree())
    except FileNotFoundError:
        # Create the directory if not exist
        try:
            os.makedirs(resource_directory + "\\GeneratedFiles\\Oracles\\" + repository_owner + "\\" + repository_name)
        except OSError as error:
            pass
        # Write on a file the Abstract Syntax Tree of all system
        with open(resource_directory + "\\GeneratedFiles\\Oracles\\" +
                  repository_owner + "\\SystemObject.xml", "w", encoding='utf-8') as f:
            f.write(bytecode.get_system_object().abstract_syntax_tree())

    #
    # Detectors
    #
    SuperclassDetector(bytecode.get_system_object())
    ConstructorDetector(bytecode.get_system_object())
    VariableDetector(bytecode.get_system_object())
    MethodOriginDetector(bytecode.get_system_object())
    TypeDetector(bytecode.get_system_object())

    # Write on a file the Abstract Syntax Tree (TypeChecked)
    with open(resource_directory + "\\GeneratedFiles\\Oracles\\" +
              repository_owner + "\\SystemObjectAdjusted.xml", "w", encoding='utf-8') as f:
        f.write(bytecode.get_system_object().abstract_syntax_tree())

    print("Number of classes to control: " + str(len(bytecode.get_system_object().get_class_names())))
    string_to_return = string_to_return + "Number of controlled class: " + str(
        len(bytecode.get_system_object().get_class_names()))

    #
    # Design Pattern Detection
    #
    detection = DesignPatternDetection()
    print("Generating System....")
    # Get informations from system object
    system_generator = SystemGenerator(bytecode.get_system_object())
    print("Detection...")
    pattern_results = list()
    # Get the list of Design Patterns
    pattern_list = list(DesignPattern)
    for pattern in pattern_list:
        print("Control Design Pattern: " + pattern.name)
        pattern_name = pattern.name
        pattern_result = PatternResult(pattern_name)
        # For now there is only one descriptor
        pattern_descriptor = detection.set_design_pattern(pattern_name)
        # TODO da vedere in quanto dipende dalle gerarchie che in python sono multi
        if pattern_descriptor.get_number_of_hierarchies() == 2:
            # Create the cluster set from system generator with pattern selected
            cluster_set = system_generator.generate_cluster_set(pattern_descriptor).get_cluster_set()
            for entry in cluster_set:
                # Get the hierarchies
                hierarchies_matrix_container = system_generator.get_hierarchies_matrix_container(
                    entry.get_hierarchy_list())
                # TODO da vedere in quanto dipende dalle gerarchie che in python sono multi
                if len(hierarchies_matrix_container.get_association_matrix()) > 2:
                    print(hierarchies_matrix_container.get_association_matrix().to_string())
                    string_to_return = string_to_return + "\nThis instance have a multiple hierarchy, this is the structure:"
                    string_to_return = string_to_return + str(hierarchies_matrix_container) + "\n"
                    continue
                # Construct the association matrix
                pattern_descriptor.set_association_matrix(
                    pd.DataFrame(pattern_descriptor.get_association_matrix().values,
                                 index=hierarchies_matrix_container.get_association_matrix().index,
                                 columns=hierarchies_matrix_container.get_association_matrix().columns))
                # Detect of design pattern selected
                detection.generate_results(hierarchies_matrix_container, pattern_descriptor, pattern_result)
        pattern_results.append(pattern_result)

    print("End Detection")

    #
    # Results
    #
    string_result = repository_owner + "\\" + repository_name
    if branch_name != "":
        string_result = string_result + "\\" + branch_name
    print("\nFor " + string_result + " are individuated the current instances:")
    for pattern_individuated in pattern_results:
        string_to_return = string_to_return + "\n- Instance of: " + pattern_individuated.get_pattern_name() + "\n"
        print(" - Instance of: " + pattern_individuated.get_pattern_name())
        if len(pattern_individuated.get_pattern_instances()) == 0:
            string_to_return = string_to_return + "   Nothing\n"
            print("   Nothing")
        for pattern_instance in pattern_individuated.get_pattern_instances():
            print("  ", pattern_instance.get_instance_counter(), " instance: ")
            print("  " + str(pattern_instance))
            string_to_return = string_to_return + "  " + str(pattern_instance.get_instance_counter()) + " instance: "
            string_to_return = string_to_return + "   " + str(pattern_instance) + "\n"
        string_to_return = string_to_return + "\n"
        string_to_return = string_to_return + "------------------------------------------------------------------------------"
        string_to_return = string_to_return + "\n"
        print("----------------------------------------")
    return string_to_return


def execute_test(test_name, debug_active):
    # Compile Oracle Files because there isn't invoked from any class
    Compiler.compile_file(current_directory + "\\Oracle\\Adapter\\AdapterPattern.py")
    Compiler.compile_repository_files(current_directory + "\\Oracle\\AdapterExtended")
    Compiler.compile_file(current_directory + "\\Oracle\\Classes\\Classes.py")
    Compiler.compile_file(current_directory + "\\Oracle\\Test\\__init__.py")

    bytecode = ReadBytecode(debug_active)
    # Download the file from a repository
    bytecode.select_file(current_directory + "\\Oracle\\" + test_name, resource_directory + "\\Oracles\\" + test_name)

    # Write on a file the Abstract Syntax Tree of all system
    with open(resource_directory + "\\Oracles\\" +
              test_name + "\\SystemObject.xml", "w", encoding='utf-8') as f:
        f.write(bytecode.get_system_object().abstract_syntax_tree())

    #
    # Detectors
    #
    SuperclassDetector(bytecode.get_system_object())
    ConstructorDetector(bytecode.get_system_object())
    VariableDetector(bytecode.get_system_object())
    MethodOriginDetector(bytecode.get_system_object())
    TypeDetector(bytecode.get_system_object())

    # Write on a file the Abstract Syntax Tree (TypeChecked)
    with open(resource_directory + "\\Oracles\\" +
              test_name + "\\SystemObjectAdjusted.xml", "w", encoding='utf-8') as f:
        f.write(bytecode.get_system_object().abstract_syntax_tree())

    #
    # Design Pattern Detection
    #
    detection = DesignPatternDetection()
    # Get informations from system object
    system_generator = SystemGenerator(bytecode.get_system_object())
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
            cluster_set = system_generator.generate_cluster_set(pattern_descriptor).get_cluster_set()
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
    print("\nFor " + test_name + " are individuated the current instances:")
    for pattern_individuated in pattern_results:
        print("\t- Instance of: " + pattern_individuated.get_pattern_name())
        for pattern_instance in pattern_individuated.get_pattern_instances():
            print("\t\tNumber of instances: ", pattern_instance.get_instance_counter())
            print("\t\t" + str(pattern_instance))
        print("----------------------------------------")


def execute_niche(args):
    debug_active, start, end = args
    niche_df = pd.read_excel(resource_directory + "/NICHE.xlsx")
    counter = 0

    # Write on a file the Abstract Syntax Tree of all system
    with open(resource_directory + "\\GeneratedFiles\\Oracles\\" + "log.txt", "a", encoding='utf-8') as f:
        for repository in niche_df["GitHub Repo"]:
            if counter < start:
                counter = counter + 1
                continue
            if counter == end:
                break
            string_to_add = single_execution(repository, debug_active)
            f.write("[" + str(counter + 1) + "] " + repository + "\n" + string_to_add)
            counter = counter + 1


def single_execution(repository, debug_active):
    split = repository.split("/")
    return execute(split[0], split[1], "", debug_active)


# execute_test("AdapterExtended", 0)
# execute_test("Adapter", 0)
# execute_test("Test", 0)
# with open(resource_directory + "\\GeneratedFiles\\Oracles\\" + "log.txt", "w", encoding='utf-8') as f:
#     single_execution("allenai/scibert", 0, f)
# execute_niche(debug_active=0, start=0, end=10)
# execute_niche(debug_active=0, start=10, end=20)
# execute_niche(debug_active=0, start=20, end=30)
# execute_niche(debug_active=0, start=30, end=40)
# execute_niche(debug_active=0, start=40, end=50)
# execute_niche(debug_active=0, start=50, end=60)
# execute_niche(debug_active=0, start=63, end=70)
# execute_niche(debug_active=0, start=0, end=70)
if __name__ == '__main__':
    number_of_splits = 6
    with Pool(number_of_splits) as p:
        valori = [(0, i * 10, (i + 1) * 10) for i in range(number_of_splits)]  # Crea una lista di tuple
        p.map(execute_niche, valori)
