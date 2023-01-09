import sys
from dataclasses import dataclass
from typing import List

from lark import Lark, Transformer, v_args, ast_utils, UnexpectedInput


class _Ast(ast_utils.Ast):
    # This will be skipped by create_transformer(), because it starts with an underscore
    pass


@dataclass
class Type(_Ast):
    pass


@dataclass
class Pointer(Type):
    type: Type

    def __str__(self):
        return f"{self.type}*"


@dataclass
class TypeList(ast_utils.AsList):
    children: List[Type]


@dataclass
class FuncPtr(Type):
    type: Type
    type_list: TypeList

    def __str__(self):
        params = ', '.join([str(x) for x in self.type_list.children])
        return f"function {self.type}({params})"


@dataclass
class Struct(Type):
    type: Type

    def __str__(self):
        return str(self.type)


@dataclass
class Array(Type):
    type: Type
    size: int

    def __str__(self):
        return f"{self.type}[{self.size}]"


@dataclass
class Const(Type):
    type: Type

    def __str__(self):
        return str(self.type)


@dataclass
class Volatile(Type):
    type: Type

    def __str__(self):
        return str(self.type)


@dataclass
class Identifier(Type):
    name: str

    def __str__(self):
        return self.name


class ToAst(Transformer):
    def signed_char(self, _):
        return "i8"

    def unsigned_char(self, _):
        return "u8"

    def signed_short(self, _):
        return "i16"

    def unsigned_short(self, _):
        return "u16"

    def signed_int(self, _):
        return "i32"

    def unsigned_int(self, _):
        return "u32"

    def signed_long(self, _):
        return "i64"

    def unsigned_long(self, _):
        return "u64"

    def float(self, _):
        return "float"

    def double(self, _):
        return "double"

    @v_args(inline=True)
    def start(self, x):
        return x


class TypeParser:
    def __init__(self):
        type_grammar = r"""
                    start : type
                    ?type : func_ptr | const | volatile | pointer | numeric | struct | identifier | array
                    func_ptr : type "(*)" type_list
                    type_list : "(" (type ("," type)*)?  ")"
                    array : type "[" INT "]"
                    const : "const" type
                    volatile : "volatile" type
                    pointer : type "*"
                    struct : "struct" type
                    ?numeric : char | short | int | long | float | double
                    ?char : signed_char | unsigned_char
                    signed_char : "signed"? "char"
                    unsigned_char : "unsigned" "char"
                    ?short : signed_short | unsigned_short
                    signed_short: "signed"? "short" "int"?
                    unsigned_short: "unsigned" "short" "int"?
                    ?int : signed_int | unsigned_int
                    signed_int: "signed"? "int"
                    unsigned_int: "unsigned" "int"?
                    ?long : signed_long | unsigned_long
                    signed_long: "signed"? "long"+ "int"?
                    unsigned_long: "unsigned" "long"+ "int"?
                    float: "float"
                    double: "long"? "double"
                    identifier : IDENTIFIER
                    IDENTIFIER : /[a-zA-Z_][a-zA-Z0-9_]*/
                    %import common.WS
                    %import common.INT
                    %ignore WS
                """
        self.type_parser = Lark(type_grammar, parser='earley', lexer='basic', propagate_positions=False, maybe_placeholders=False)
        self.transformer = ast_utils.create_transformer(sys.modules[__name__], ToAst())


    def parse(self, type):
        try:
            tree = self.type_parser.parse(type)
            return str(self.transformer.transform(tree))
        except UnexpectedInput as u:
            # print(f"warning: unable to parse type `{type}`")
            # print(u)
            return None
