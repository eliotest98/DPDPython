import os

from Core.ReadBytecode import ReadBytecode

# Get the current directory
current_directory = os.getcwd().replace("\\Core", "") + "\\Oracle\\Adapter"

bytecode = ReadBytecode()
bytecode.select_file(current_directory)
