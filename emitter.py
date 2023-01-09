from dataclasses import dataclass
from typing import Callable


@dataclass
class EmitterOptions:
    function_name: Callable[[str], str]
    parameter_name: Callable[[str], str]
    enum_name: Callable[[str], str]


class Emitter(object):
    def __init__(self, module, class_name, namespace, options: EmitterOptions):
        self.class_name = class_name
        self.namespace = namespace
        self.module = module
        self.options = options

    def emit(self):
        s = ''
        s += f"namespace {self.namespace}\n"
        s += '{\n'
        s += f"\tclass {self.class_name}\n"
        s += '\t{\n'

        for d in self.module.enums.values():
            if not d.name:
                continue
            enum_name = self.options.enum_name(d.name)
            s += f"\t\tenum {enum_name}\n"
            s += '\t\t{\n'
            for c in d.constants:
                if c.comment:
                    s += f"\t\t\t// {c.comment}\n"
                if c.value:
                    s += f"\t\t\t{c.name} = {c.value},\n"
                else:
                    s += f"\t\t\t{c.name},\n"
            s += '\t\t}\n\n'

        for d in self.module.structs.values():
            if not d.name:
                continue
            s += f"\t\t[CRepr]\n"
            s += f"\t\tstruct {d.name}\n"
            s += '\t\t{\n'
            for f in d.fields:
                s += f"\t\t\t{f.type} {f.name};\n"
            s += '\t\t}\n\n'

        for d in self.module.functions.values():
            params = []
            i = 1
            for p in d.params:
                param_name = '_' * i
                if p.name:
                    param_name = self.options.parameter_name(p.name)
                param_type = p.type or '?'
                params.append(f"{param_type} {param_name}")
            name = self.options.function_name(d.name)
            s += f"\t\t[LinkName(\"{d.name}\")\n"
            s += f"\t\textern function {name}({', '.join(params)});\n\n"

        s += '\t}\n'
        s += '}\n'

        return s
