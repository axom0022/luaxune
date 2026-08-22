import math

class vm:
    def __init__(self, api):
        self.api = api
        self.stack = []
        self.env = {}
        self.pc = 0
        self.bytecode = []
        self.frames = []
        self.globals = api.globals

    def run(self, bytecode, env=None):
        self.bytecode = bytecode
        self.pc = 0
        if env:
            self.env = env
        else:
            self.env = self.globals.copy()
        while self.pc < len(self.bytecode):
            op = self.bytecode[self.pc]
            self.pc += 1
            self.execop(op)
        return self.stack[-1] if self.stack else None

    def execop(self, op):
        cmd = op[0]
        if cmd == 'push_number':
            self.stack.append(op[1])
        elif cmd == 'push_string':
            self.stack.append(op[1])
        elif cmd == 'push_boolean':
            self.stack.append(op[1])
        elif cmd == 'push_nil':
            self.stack.append(None)
        elif cmd == 'load_var':
            name = op[1]
            if name in self.env:
                self.stack.append(self.env[name])
            else:
                self.stack.append(None)
        elif cmd == 'store_local':
            name = op[1]
            if self.stack:
                self.env[name] = self.stack.pop()
            else:
                self.env[name] = None
        elif cmd == 'pop':
            if self.stack:
                self.stack.pop()
        elif cmd == 'return':
            count = op[1]
            vals = []
            for _ in range(count):
                if self.stack:
                    vals.insert(0, self.stack.pop())
            if count == 0:
                self.stack.append(None)
            elif count == 1:
                self.stack.append(vals[0])
            else:
                self.stack.append(tuple(vals))
        elif cmd == 'function':
            name = op[1]
            params = op[2]
            self.env[name] = lambda *args: self.callfunction(name, params, args)
        elif cmd == 'endfunction':
            pass
        elif cmd == 'jump_if_false':
            target = op[1]
            if self.stack and not self.stack[-1]:
                self.pc += target
        elif cmd == 'jump':
            target = op[1]
            self.pc += target
        elif cmd == 'loop_start':
            self.stack.append(self.pc)
        elif cmd == 'loop_end':
            if self.stack:
                self.pc = self.stack.pop()
        elif cmd == 'for_prepare':
            var = op[1]
            step = self.stack.pop() if self.stack else 1
            end = self.stack.pop() if self.stack else 0
            start = self.stack.pop() if self.stack else 0
            self.env[var] = start
            self.stack.append(start)
            self.stack.append(end)
            self.stack.append(step)
        elif cmd == 'get_property':
            prop = op[1]
            obj = self.stack.pop() if self.stack else None
            if obj is not None:
                if hasattr(obj, prop):
                    val = getattr(obj, prop)
                elif hasattr(obj, 'get'):
                    val = obj.get(prop)
                else:
                    val = None
            else:
                val = None
            self.stack.append(val)
        elif cmd == 'get_index':
            idx = self.stack.pop() if self.stack else None
            obj = self.stack.pop() if self.stack else None
            if obj is not None:
                if isinstance(obj, dict):
                    val = obj.get(idx)
                elif hasattr(obj, '__getitem__'):
                    try:
                        val = obj[idx]
                    except:
                        val = None
                else:
                    val = None
            else:
                val = None
            self.stack.append(val)
        elif cmd == 'add':
            b = self.stack.pop() if self.stack else 0
            a = self.stack.pop() if self.stack else 0
            self.stack.append(a + b)
        elif cmd == 'sub':
            b = self.stack.pop() if self.stack else 0
            a = self.stack.pop() if self.stack else 0
            self.stack.append(a - b)
        elif cmd == 'mul':
            b = self.stack.pop() if self.stack else 0
            a = self.stack.pop() if self.stack else 0
            self.stack.append(a * b)
        elif cmd == 'div':
            b = self.stack.pop() if self.stack else 0
            a = self.stack.pop() if self.stack else 0
            self.stack.append(a / b if b != 0 else 0)
        elif cmd == 'mod':
            b = self.stack.pop() if self.stack else 0
            a = self.stack.pop() if self.stack else 0
            self.stack.append(a % b if b != 0 else 0)
        elif cmd == 'pow':
            b = self.stack.pop() if self.stack else 0
            a = self.stack.pop() if self.stack else 0
            self.stack.append(math.pow(a, b))
        elif cmd == 'concat':
            b = self.stack.pop() if self.stack else ''
            a = self.stack.pop() if self.stack else ''
            self.stack.append(str(a) + str(b))
        elif cmd == 'lt':
            b = self.stack.pop() if self.stack else 0
            a = self.stack.pop() if self.stack else 0
            self.stack.append(a < b)
        elif cmd == 'le':
            b = self.stack.pop() if self.stack else 0
            a = self.stack.pop() if self.stack else 0
            self.stack.append(a <= b)
        elif cmd == 'gt':
            b = self.stack.pop() if self.stack else 0
            a = self.stack.pop() if self.stack else 0
            self.stack.append(a > b)
        elif cmd == 'ge':
            b = self.stack.pop() if self.stack else 0
            a = self.stack.pop() if self.stack else 0
            self.stack.append(a >= b)
        elif cmd == 'eq':
            b = self.stack.pop() if self.stack else 0
            a = self.stack.pop() if self.stack else 0
            self.stack.append(a == b)
        elif cmd == 'ne':
            b = self.stack.pop() if self.stack else 0
            a = self.stack.pop() if self.stack else 0
            self.stack.append(a != b)
        elif cmd == 'and':
            b = self.stack.pop() if self.stack else False
            a = self.stack.pop() if self.stack else False
            self.stack.append(a and b)
        elif cmd == 'or':
            b = self.stack.pop() if self.stack else False
            a = self.stack.pop() if self.stack else False
            self.stack.append(a or b)

    def callfunction(self, name, params, args):
        return None
