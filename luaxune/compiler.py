class compiler:
    def compile(self, ast):
        bytecode = []
        self.compilenode(ast, bytecode)
        return bytecode

    def compilenode(self, node, bytecode):
        t = node['type']
        if t == 'chunk':
            for child in node.get('body', []):
                self.compilenode(child, bytecode)
        elif t == 'local':
            for i, name in enumerate(node['names']):
                if i < len(node['values']):
                    self.compilenode(node['values'][i], bytecode)
                else:
                    bytecode.append(('push_nil',))
                bytecode.append(('store_local', name))
        elif t == 'function':
            bytecode.append(('function', node.get('name'), node.get('params', [])))
            for stmt in node.get('body', []):
                self.compilenode(stmt, bytecode)
            bytecode.append(('endfunction',))
        elif t == 'if':
            self.compilenode(node['condition'], bytecode)
            bytecode.append(('jump_if_false', 0))
            for stmt in node.get('then', []):
                self.compilenode(stmt, bytecode)
            bytecode.append(('jump', 0))
            for stmt in node.get('else', []):
                self.compilenode(stmt, bytecode)
        elif t == 'while':
            bytecode.append(('loop_start',))
            self.compilenode(node['condition'], bytecode)
            bytecode.append(('jump_if_false', 0))
            for stmt in node.get('body', []):
                self.compilenode(stmt, bytecode)
            bytecode.append(('jump', 0))
            bytecode.append(('loop_end',))
        elif t == 'for':
            self.compilenode(node['start'], bytecode)
            self.compilenode(node['end'], bytecode)
            step = node.get('step')
            if step:
                self.compilenode(step, bytecode)
            else:
                bytecode.append(('push_number', 1))
            bytecode.append(('for_prepare', node['var']))
            bytecode.append(('loop_start',))
            for stmt in node.get('body', []):
                self.compilenode(stmt, bytecode)
            bytecode.append(('loop_end',))
        elif t == 'repeat':
            bytecode.append(('loop_start',))
            for stmt in node.get('body', []):
                self.compilenode(stmt, bytecode)
            self.compilenode(node['condition'], bytecode)
            bytecode.append(('jump_if_false', 0))
            bytecode.append(('loop_end',))
        elif t == 'return':
            for val in node.get('values', []):
                self.compilenode(val, bytecode)
            bytecode.append(('return', len(node.get('values', []))))
        elif t == 'expression':
            self.compilenode(node['value'], bytecode)
            bytecode.append(('pop',))
        elif t == 'number':
            bytecode.append(('push_number', node['value']))
        elif t == 'string':
            bytecode.append(('push_string', node['value']))
        elif t == 'boolean':
            bytecode.append(('push_boolean', node['value']))
        elif t == 'nil':
            bytecode.append(('push_nil',))
        elif t == 'identifier':
            bytecode.append(('load_var', node['value']))
        elif t == 'grouped':
            self.compilenode(node['value'], bytecode)
        elif t == 'property':
            self.compilenode(node['object'], bytecode)
            bytecode.append(('get_property', node['property']))
        elif t == 'index':
            self.compilenode(node['object'], bytecode)
            self.compilenode(node['index'], bytecode)
            bytecode.append(('get_index',))
        elif t == 'binop':
            self.compilenode(node['left'], bytecode)
            self.compilenode(node['right'], bytecode)
            op = node['op']
            if op == '+':
                bytecode.append(('add',))
            elif op == '-':
                bytecode.append(('sub',))
            elif op == '*':
                bytecode.append(('mul',))
            elif op == '/':
                bytecode.append(('div',))
            elif op == '%':
                bytecode.append(('mod',))
            elif op == '^':
                bytecode.append(('pow',))
            elif op == '..':
                bytecode.append(('concat',))
            elif op == '<':
                bytecode.append(('lt',))
            elif op == '<=':
                bytecode.append(('le',))
            elif op == '>':
                bytecode.append(('gt',))
            elif op == '>=':
                bytecode.append(('ge',))
            elif op == '==':
                bytecode.append(('eq',))
            elif op == '~=':
                bytecode.append(('ne',))
            elif op == 'and':
                bytecode.append(('and',))
            elif op == 'or':
                bytecode.append(('or',))
            else:
                bytecode.append(('push_nil',))
