# DPDPython
Design Pattern Detector for Python

The project is divided into two main packages:
 - python: in this folder there is the source code of tool
 - resources: in this folder there is documents or file auto generated

In python folder there are some packages:
 - Compiler: in this package there is a class for compile a python code (this compiler is used for Github repositories)
 - Core: in this package there are the main classes for execute the detection and all the operations for detect a pattern
 - Descriptors: in this package there are the classes who represent a DesignPattern instance for comparison algorithm
 - Detectors: in this package there are the classes for detect a design pattern and a superclass
 - Downloader: in this package there are the classes for manage the github repositories
 - Objects: in this package there are all file Objects for create the Abstract Syntax Tree
 - Oracle: in this package there are some classes for test
 - Readers: in this package there are the readers for read the bytecode
 - Utils: in this package there are some utils class

## How to use:
### Direct Execution:
1. Open the subfolder Core at path: src.main.python.Core
2. Execute the Starter file
### Pycharm:
1. Execute "Start" configuration
### Docker:
1. Execute "Dockerfile" configuration
2. Open the container created in docker desktop
3. Open the terminal
4. Execute "python3 /app/src/main/python/Core/Starter.py"

