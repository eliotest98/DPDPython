# This class represent all files in a repository
# Is formed from:
# - dirs
# - files
class SystemObject:
    dirs_map = {}
    file_list = list()

    def __init__(self):
        self.dirs_map = {}
        self.file_list = list()

    def add_class(self, file_object, directory):
        if directory in self.dirs_map:
            self.dirs_map[directory].append(file_object)
        else:
            self.dirs_map[directory] = [file_object]
        self.file_list.append(file_object)

    def get_file_list(self):
        return self.file_list

    def abstract_syntax_tree(self):
        return_string = "<SYSTEM>\n"
        for chiave, valore in self.dirs_map.items():
            return_string = return_string + "<DIR> (id," + chiave + ")\n"
            for file_obj in valore:
                return_string = return_string + file_obj.abstract_syntax_tree()
            return_string = return_string + "</DIR>\n"
        return_string = return_string + "</SYSTEM>"
        return return_string
