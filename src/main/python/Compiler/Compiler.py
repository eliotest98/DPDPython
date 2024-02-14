import os
import py_compile


# This method compile a file
def compile_file(path):
    py_compile.compile(path)


# This method compile all repository files
def compile_repository_files(path):
    if os.path.isdir(path):
        for dir in os.listdir(path):
            if os.path.isfile(path + "\\" + dir):
                compile_repository_files(path + "\\" + dir)
            else:
                if os.listdir(path + "\\" + dir):
                    compile_repository_files(path + "\\" + dir)
                else:
                    compile_repository_files(path + "\\" + dir)
    else:
        compile_file(path)