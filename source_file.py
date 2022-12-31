import json
import subprocess


class SourceFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.ast = self.build_ast()

    def build_ast(self):
        print(f"info: generating AST for {self.filename}")
        result = subprocess.run(['clang', '-E', '-Xclang', '-ast-dump=json', '-nostdinc', '-fno-builtin', self.filename], stdout=subprocess.PIPE)
        data = result.stdout.decode('utf-8')
        print(f"info: parsing AST for {self.filename}")
        return json.loads(data)
