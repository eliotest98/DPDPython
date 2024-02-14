from Descriptors.MatrixContainer import MatrixContainer
from Detector.HierarchyDetection import HierarchyDetection
from Detector.SuperclassDetector import SuperclassDetector


class SystemGenerator:

    system_object = ""
    matrix_container = ""
    hierarchy_list = list()

    def __init__(self, system_object):
        self.system_object = system_object
        self.matrix_container = MatrixContainer()
        #SuperclassDetector()
        self.hierarchy_list = HierarchyDetection(system_object)