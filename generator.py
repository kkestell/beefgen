from dataclasses import dataclass
from typing import List

from module import Module
from source_file import SourceFile
from type_parser import TypeParser


@dataclass
class Location:
    offset: int
    col: int
    tokLen: int


@dataclass
class Range:
    begin: Location
    end: Location


@dataclass
class Constant:
    range: Range
    name: str
    value: str
    comment: str


@dataclass
class Enum:
    id: str
    range: Range
    name: str
    constants: List[Constant]


@dataclass
class Parameter:
    range: Range
    name: str
    type: str

    def as_beef(self):
        return f"{self.type} {self.name}"


@dataclass
class Function:
    id: str
    range: Range
    name: str
    type: str
    params: List[Parameter]

@dataclass
class Field:
    range: Range
    name: str
    type: str


@dataclass
class Struct:
    id: str
    range: Range
    name: str
    fields: List[Field]


@dataclass
class Typedef:
    id: str
    range: Range
    name: str
    type: str


class Generator(object):
    def __init__(self, h_file, options={}):
        self.h_file = SourceFile(h_file)
        self.module = Module()
        self.type_parser = TypeParser()
        self.options = options

    def generate(self):
        for decl in self.h_file.ast['inner']:
            if decl.get('isImplicit', False):
                continue

            if not decl['loc']:
                continue

            match decl['kind']:
                case 'EnumDecl':
                    self.generate_enum(decl)
                case 'FunctionDecl':
                    self.generate_function(decl)
                case 'RecordDecl':
                    self.generate_struct(decl)
                case 'TypedefDecl':
                    self.generate_typedef(decl)

        return self.module

    def generate_enum(self, decl):
        consts = []
        for const_decl in decl.get('inner', []):
            if const_decl['kind'] == 'EnumConstantDecl':
                constant = self.generate_enum_constant(const_decl)
                consts.append(constant)

        self.module.add_enum(Enum(decl['id'], decl['range'], decl.get('name', None), consts))

    def generate_function(self, decl):
        # print(f"info: generating function {decl['name']} from {decl['loc']}")
        function_name = decl.get('name', None)
        if function_name and function_name.startswith('_'):
            return
        params = []
        for param_decl in decl.get('inner', []):
            if param_decl['kind'] != 'ParmVarDecl':
                continue
            param = self.generate_function_parameter(param_decl)
            params.append(param)

        self.module.add_function(Function(decl['id'], decl['range'], function_name, decl['type']['qualType'], params))

    def generate_struct(self, decl):
        struct_name = decl.get('name', None)
        # print(f"info: generating struct {struct_name} from {decl['loc']}")
        fields = []
        for field_decl in decl.get('inner', []):
            if field_decl['kind'] != 'FieldDecl':
                continue
            field = self.generate_struct_field(field_decl)
            fields.append(field)

        self.module.add_struct(Struct(decl['id'], decl['range'], struct_name, fields))

    def generate_typedef(self, decl):
        # print(f"info: generating typedef {decl['name']} from {decl['loc']}")
        if decl.get('inner', None):
            if decl['inner'][0]['kind'] == 'ElaboratedType':
                #print(f"warning: unsupported inner node {decl['inner'][0]['kind']}")
                if 'ownedTagDecl' in decl['inner'][0]:
                    owned_by = decl['inner'][0]['ownedTagDecl']
                    if owned_by['kind'] == 'RecordDecl':
                        struct = next((x for x in self.module.structs.values() if x.id == owned_by['id']))
                        struct.name = decl['name']
                    elif owned_by['kind'] == 'EnumDecl':
                        enum = [x for x in self.module.enums.values() if x.id == owned_by['id']][0]
                        enum.name = decl['name']

        self.module.add_typedef(Typedef(decl['id'], decl['range'], decl['name'], decl['type']['qualType']))

    def generate_struct_field(self, decl):
        field_type = self.type_parser.parse(decl['type']['qualType'])
        return Field(decl['range'], decl['name'], field_type)

    def generate_function_parameter(self, decl):
        param_type = self.type_parser.parse(decl['type']['qualType'])
        return Parameter(decl['range'], decl.get('name', None), param_type)

    def generate_enum_constant(self, decl):
        value = None
        comment = None
        if 'inner' in decl:
            for inner in decl['inner']:
                if inner['kind'] == 'ConstantExpr':
                    value = self.parse_enum_constant_value(inner)
                elif inner['kind'] == 'FullComment':
                    comment = self.parse_enum_constant_comment(inner)

        return Constant(decl['range'], decl['name'], value, comment)

    def parse_enum_constant_value(self, const_expr):
        if 'inner' in const_expr:
            int_literal = const_expr['inner'][0]
            if int_literal['kind'] != 'IntegerLiteral':
                print(f"warning: skipping {int_literal['kind']} in enum constant expression")
            else:
                return int_literal['value']
    
    def parse_enum_constant_comment(self, const_expr):
        para_comment = const_expr['inner'][0]
        if para_comment['kind'] == 'ParagraphComment':
            text_comment = para_comment['inner'][0]
            if text_comment['kind'] == 'TextComment':
                comment = text_comment['text'].strip()
                if comment != '':
                    return comment
        return None
