from Utils.DesignPattern import DesignPattern


class PatternResult:

    pattern_name = ""
    instances = list()

    def __init__(self, pattern_name):
        self.pattern_name = pattern_name
        self.instances = list()

    def add_instance(self, instance):
        self.instances.append(instance)
        instance.set_instance_counter(len(self.instances))

    def contains_instance(self, instance):
        return instance in self.instances

    def get_pattern_name(self):
        return self.pattern_name

    def get_pattern_instances(self):
        return self.instances
