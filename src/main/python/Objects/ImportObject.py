# This class represent the import/from instance
# A import is formed from:
# - a import key
# - a list of strings
# A from is formed from:
# - a from key
# - a string
# - a import key
# - a list of strings
class ImportObject:
    from_name = ""
    string_list = list()
    as_name = ""

    def __init__(self):
        self.from_name = ""
        self.as_name = ""
        self.string_list = list()

    def set_from_name(self, from_name):
        self.from_name = from_name

    def get_from_name(self):
        return self.from_name

    def set_as_name(self, as_name):
        self.as_name = as_name

    def get_as_name(self):
        return self.as_name

    def add_string(self, string):
        if isinstance(string, tuple):
            for str in string:
                self.string_list.append(str)
        else:
            self.string_list.append(string)

    def get_import_list(self):
        return self.string_list

    def abstract_syntax_tree(self, number_of_tabs):
        string_tabs = (number_of_tabs + 1) * "\t"
        internal_string_tabs = string_tabs + "\t"
        string_to_return = ""
        if self.from_name != "":
            string_to_return = string_to_return + string_tabs + "<FROM>(id," + str(self.from_name) + ")\n"
            if len(self.string_list) != 0:
                for string in self.string_list:
                    string_to_return = string_to_return + internal_string_tabs + "<IMPORT>(id," + str(
                        string) + ")</IMPORT>\n"
            string_to_return = string_to_return + string_tabs + "</FROM>"
        else:
            if len(self.string_list) != 0:
                for string in self.string_list:
                    if self.as_name != "":
                        string_to_return = string_to_return + string_tabs + "<IMPORT>(id," + string + ")" + "\n"
                        string_to_return = string_to_return + internal_string_tabs + "<AS>(id, " + self.as_name + ")</AS>" + "\n"
                        string_to_return = string_to_return + string_tabs + "</IMPORT>"
                    else:
                        string_to_return = string_to_return + string_tabs + "<IMPORT>(id," + string + ")</IMPORT>"
        return string_to_return
