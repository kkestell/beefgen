class Module(object):
    def __init__(self):
        self.enums = {}
        self.functions = {}
        self.structs = {}
        self.typedefs = {}

    def add_enum(self, enum):
        self.enums[enum.id] = enum

    def add_function(self, function):
        self.functions[function.id] = function

    def add_struct(self, struct):
        self.structs[struct.id] = struct

    def add_typedef(self, typedef):
        self.typedefs[typedef.id] = typedef
