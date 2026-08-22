class typechecker:
    def __init__(self):
        self.types = {}
        self.scope = [{}]
        self.errors = []

    def check(self, ast):
        self.errors = []
        self._check_node(ast)
        return self.errors

    def _check_node(self, node):
        t = node.get('type')
        if t == 'chunk':
            for stmt in node.get('body', []):
                self._check_node(stmt)
        elif t == 'local':
            for i, name in enumerate(node.get('names', [])):
                typ = node.get('types', [None])[i] if 'types' in node else None
                val = node.get('values', [None])[i] if i < len(node.get('values', [])) else None
                if typ:
                    self.scope[-1][name] = typ
                if val:
                    valtype = self._infer_type(val)
                    if typ and valtype != typ and valtype != 'nil':
                        self.errors.append(f'Type mismatch: {name} expected {typ} got {valtype}')
        elif t == 'function':
            params = node.get('params', [])
            paramtypes = node.get('paramtypes', [None] * len(params))
            rettype = node.get('rettype', None)
            self.scope.append({})
            for i, p in enumerate(params):
                if paramtypes[i]:
                    self.scope[-1][p] = paramtypes[i]
            for stmt in node.get('body', []):
                self._check_node(stmt)
            self.scope.pop()
        elif t == 'assignment':
            var = node.get('var')
            val = node.get('value')
            if var and val:
                vartype = self._resolve_type(var)
                valtype = self._infer_type(val)
                if vartype and valtype and vartype != valtype and valtype != 'nil':
                    self.errors.append(f'Type mismatch: {var} expected {vartype} got {valtype}')
        elif t == 'return':
            for val in node.get('values', []):
                self._infer_type(val)

    def _resolve_type(self, name):
        for scope in reversed(self.scope):
            if name in scope:
                return scope[name]
        return None

    def _infer_type(self, expr):
        if not expr:
            return 'nil'
        if expr.get('type') == 'number':
            return 'number'
        if expr.get('type') == 'string':
            return 'string'
        if expr.get('type') == 'boolean':
            return 'boolean'
        if expr.get('type') == 'nil':
            return 'nil'
        if expr.get('type') == 'identifier':
            return self._resolve_type(expr.get('value')) or 'any'
        if expr.get('type') == 'binop':
            left = self._infer_type(expr.get('left'))
            right = self._infer_type(expr.get('right'))
            if left == 'number' and right == 'number':
                return 'number'
            if left == 'string' or right == 'string':
                return 'string'
            if left == 'boolean' and right == 'boolean':
                return 'boolean'
            return 'any'
        if expr.get('type') == 'unop':
            return self._infer_type(expr.get('operand'))
        if expr.get('type') == 'call':
            return 'any'
        if expr.get('type') == 'table':
            return 'table'
        return 'any'
