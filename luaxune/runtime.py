from .parser import parser
from .compiler import compiler
from .vm import vm
from .api import createapi

class luaruntime:
    def __init__(self):
        self.api = createapi()
        self.vm = vm(self.api)
        self.parser = parser()
        self.compiler = compiler()

    def execute(self, code, env=None):
        ast = self.parser.parse(code)
        bytecode = self.compiler.compile(ast)
        return self.vm.run(bytecode, env or self.api.globals)

    def executefile(self, path, env=None):
        with open(path, 'r', encoding='utf-8') as f:
            return self.execute(f.read(), env)
