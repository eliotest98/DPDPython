from enum import Enum


class PatternInstance:
    def __init__(self):
        self.entry_set = set()
        self.instance_counter = 0

    def add_entry(self, e):
        self.entry_set.add(e)

    def get_entry_set(self):
        return self.entry_set

    def get_role_iterator(self):
        return iter(self.entry_set)

    def get_instance_counter(self):
        return self.instance_counter

    def set_instance_counter(self, instance_counter):
        self.instance_counter = instance_counter

    def __eq__(self, o):
        if isinstance(o, PatternInstance):
            for e in o.entry_set:
                if e not in self.entry_set:
                    return False
            return True
        return False

    def __str__(self):
        return " | ".join(str(e) for e in self.entry_set)


class Entry:
    def __init__(self, role_type, role_name, element_name, position):
        self.role_type = role_type
        self.role_name = role_name
        self.element_name = element_name
        self.position = position
        self.hash_code = 0

    def get_role_name(self):
        return self.role_name

    def get_element_name(self):
        return self.element_name

    def get_position(self):
        return self.position

    def get_role_type(self):
        return self.role_type

    def __eq__(self, o):
        if isinstance(o, Entry):
            return self.role_name == o.role_name and self.element_name == o.element_name
        return False

    def __hash__(self):
        if self.hash_code == 0:
            self.hash_code = 17
            self.hash_code = 37 * self.hash_code + hash(self.role_name)
            self.hash_code = 37 * self.hash_code + hash(self.element_name)
        return self.hash_code

    def __str__(self):
        return f"{self.role_name}: {self.element_name}"


class RoleType(Enum):
    CLASS = "CLASS"
    METHOD = "METHOD"
    FIELD = "FIELD"
