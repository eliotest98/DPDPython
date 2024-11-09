import os
import py_compile
from Downloader.ProgressionCheck import ProgressDetection

progressor = ProgressDetection()


# This method compile a file
def compile_file(path):
    try:
        py_compile.compile(path)
    except:
        pass


# This method compile all repository files
def compile_repository_files(path, terminal):
    if os.path.isdir(path):
        counter = 1
        for dir in os.listdir(path):
            progressor.update(len(os.listdir(path)), counter, "Compiling Repository Files...", terminal)
            if os.path.isfile(os.path.join(path, dir)):
                compile_repository_files(os.path.join(path, dir), terminal)
            else:
                if os.listdir(os.path.join(path, dir)):
                    compile_repository_files(os.path.join(path, dir), terminal)
                else:
                    compile_repository_files(os.path.join(path, dir), terminal)
            counter = counter + 1
    else:
        if not path.endswith(".pyc"):
            compile_file(path)
