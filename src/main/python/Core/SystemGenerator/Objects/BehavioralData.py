class Position:
    row = ""
    column = ""
    hash = ""

    def __init__(self, x, y):
        self.row = x
        self.column = y
        self.hash = hash((x, y))

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.row == other.row and self.column == other.column
        return False

    def __hash__(self):
        return self.hash

    def __str__(self):
        return f"({self.row},{self.column})"


class BehavioralData:
    method_data = {}
    field_data = {}

    def __init__(self):
        self.method_data = {}
        self.field_data = {}

    def add_method(self, row, column, mo):
        pos = Position(row, column)
        if pos in self.method_data:
            self.method_data[pos].add(mo)
        else:
            self.method_data[pos] = {mo}

    def add_methods(self, row, column, methods):
        pos = Position(row, column)
        if pos in self.method_data:
            self.method_data[pos].update(methods)
        else:
            self.method_data[pos] = methods

    def get_methods(self, row, column):
        pos = Position(row, column)
        return self.method_data.get(pos)

    def add_field(self, row, column, fo):
        pos = Position(row, column)
        if pos in self.field_data:
            self.field_data[pos].add(fo)
        else:
            self.field_data[pos] = {fo}

    def add_fields(self, row, column, fields):
        pos = Position(row, column)
        if pos in self.field_data:
            self.field_data[pos].update(fields)
        else:
            self.field_data[pos] = fields

    def get_fields(self, row, column):
        pos = Position(row, column)
        return self.field_data.get(pos)
