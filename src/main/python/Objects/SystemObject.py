import _tkinter

from Downloader.ProgressionCheck import ProgressDetection
from Objects.FileObject import FileObject


class SystemObject:
    class_list = list()
    class_name_map = {}
    progressor = ProgressDetection()

    def __init__(self):
        self.class_list = []
        self.class_name_map = {}
        self.progressor = ProgressDetection()

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

    def abstract_syntax_tree(self, terminal, ast, product):
        return_string = "<FILE_LIST>\n"
        counter = 1
        for single_file in self.class_list:
            self.progressor.update(len(self.class_list), counter, "AST Generation", terminal)

            if product:
                if single_file.get_file_name() != "":
                    if not self.is_item_in_treeview(ast, "", single_file.get_file_name()):
                        try:
                            ast.insert("", counter, single_file.get_file_name(), text=single_file.get_file_name())
                        except _tkinter.TclError:
                            pass
                    if not self.is_item_in_treeview(ast, single_file.get_file_name(), single_file.get_class_name()):
                        try:
                            ast.insert(single_file.get_file_name(), counter, single_file.get_class_name(),
                                       text=single_file.get_class_name())
                            width = ast.column("#0")["width"]
                            possible_width = (len(single_file.get_class_name()) + len(single_file.get_file_name())) * 6
                            if possible_width > width:
                                ast.column("#0", width=possible_width)
                        except _tkinter.TclError:
                            ast.insert(single_file.get_file_name(), counter, value=(single_file.get_class_name()))
                            width = ast.column("#1")["width"]
                            possible_width = (len(single_file.get_class_name()) + len(single_file.get_file_name())) * 6
                            if possible_width > width:
                                ast.column("#1", width=possible_width)
                            pass
            if isinstance(single_file, FileObject):
                return_string = return_string + "\t" + single_file.abstract_syntax_tree(1)
            counter = counter + 1
        return_string = return_string + "</FILE_LIST>"
        return return_string

    def is_item_in_treeview(self, treeview, parent, item):
        if treeview is not None:
            for child in treeview.get_children(parent):
                if treeview.item(child, 'text') == item:
                    return True
        return False
