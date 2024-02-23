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

    def __init__(self):
        self.from_name = ""
        self.string_list = list()

    def set_from_name(self, from_name):
        self.from_name = from_name

    def add_string(self, string):
        self.string_list.append(string)

    def abstract_syntax_tree(self, number_of_tabs):
        string_tabs = (number_of_tabs + 1) * "\t"
        internal_string_tabs = string_tabs + "\t"
        string_to_return = ""
        if self.from_name != "":
            string_to_return = string_to_return + string_tabs + "<FROM>(id," + self.from_name + ")\n"
            if len(self.string_list) != 0:
                for string in self.string_list:
                    string_to_return = string_to_return + internal_string_tabs + "<IMPORT>(id," + str(
                        string) + ")</IMPORT>\n"
            string_to_return = string_to_return + string_tabs + "</FROM>"
        else:
            if len(self.string_list) != 0:
                for string in self.string_list:
                    string_to_return = string_to_return + string_tabs + "<IMPORT>(id," + string + ")</IMPORT>"
        return string_to_return
