from Objects.FileObject import FileObject


class SystemObject:
    class_list = list()
    class_name_map = {}

    def __init__(self):
        self.class_list = []
        self.class_name_map = {}

    def add_class(self, c):
        key = c.get_class_name()
        if c.get_file_name() != "":
            key = c.get_file_name() + "." + key

        if key not in self.class_name_map:
            self.class_name_map[key] = len(self.class_list)
            self.class_list.append(c)
        else:
            # TODO there are some classes duplicated
            # print("Class", key)
            pass

    def get_class_object_with_class_name(self, class_name):
        pos = self.class_name_map.get(class_name)
        if pos is not None:
            return self.get_class_object_with_position(pos)
        else:
            return None

    def get_class_object_with_position(self, pos):
        return self.class_list[pos]

    def get_class_list_iterator(self):
        return iter(self.class_list)

    def get_class_number(self):
        return len(self.class_list)

    def get_position_in_class_list(self, class_name):
        pos = self.class_name_map.get(class_name)
        if pos is not None:
            return pos
        else:
            return -1

    def get_class_names(self):
        names = []
        for i in range(len(self.class_list)):
            names.append(self.get_class_object_with_position(i).get_class_name())
        return names

    def __str__(self):
        sb = []
        for class_object in self.class_list:
            sb.append(str(class_object))
            sb.append("\n" + "-" * 80 + "\n")
        return "".join(sb)

    def abstract_syntax_tree(self):
        return_string = "<FILE_LIST>\n"
        for single_file in self.class_list:
            if isinstance(single_file, FileObject):
                return_string = return_string + "\t" + single_file.abstract_syntax_tree(1)
        return_string = return_string + "</FILE_LIST>"
        return return_string
