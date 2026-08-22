import math

class vm:
    __slots__ = ('api', 'stack', 'env', 'pc', 'bytecode', 'frames', 'globals', '_handlers')
    def __init__(self, api):
        self.api = api
        self.stack = []
        self.env = {}
        self.pc = 0
        self.bytecode = []
        self.frames = []
        self.globals = api.globals
        self._handlers = {
            'push_number': self._push_number,
            'push_string': self._push_string,
            'push_boolean': self._push_boolean,
            'push_nil': self._push_nil,
            'load_var': self._load_var,
            'store_local': self._store_local,
            'pop': self._pop,
            'return': self._return,
            'function': self._function,
            'endfunction': self._endfunction,
            'jump_if_false': self._jump_if_false,
            'jump': self._jump,
            'loop_start': self._loop_start,
            'loop_end': self._loop_end,
            'for_prepare': self._for_prepare,
            'get_property': self._get_property,
            'get_index': self._get_index,
            'add': self._add,
            'sub': self._sub,
            'mul': self._mul,
            'div': self._div,
            'mod': self._mod,
            'pow': self._pow,
            'concat': self._concat,
            'lt': self._lt,
            'le': self._le,
            'gt': self._gt,
            'ge': self._ge,
            'eq': self._eq,
            'ne': self._ne,
            'and': self._and,
            'or': self._or,
        }

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
            handler = self._handlers.get(op[0])
            if handler:
                handler(op)
        return self.stack[-1] if self.stack else None

    def _push_number(self, op): self.stack.append(op[1])
    def _push_string(self, op): self.stack.append(op[1])
    def _push_boolean(self, op): self.stack.append(op[1])
    def _push_nil(self, op): self.stack.append(None)
    def _load_var(self, op):
        name = op[1]
        if name in self.env:
            self.stack.append(self.env[name])
        else:
            self.stack.append(None)
    def _store_local(self, op):
        name = op[1]
        if self.stack:
            self.env[name] = self.stack.pop()
        else:
            self.env[name] = None
    def _pop(self, op):
        if self.stack:
            self.stack.pop()
    def _return(self, op):
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
    def _function(self, op):
        name = op[1]
        params = op[2]
        self.env[name] = lambda *args: self.callfunction(name, params, args)
    def _endfunction(self, op): pass
    def _jump_if_false(self, op):
        target = op[1]
        if self.stack and not self.stack[-1]:
            self.pc += target
    def _jump(self, op):
        self.pc += op[1]
    def _loop_start(self, op): self.stack.append(self.pc)
    def _loop_end(self, op):
        if self.stack:
            self.pc = self.stack.pop()
    def _for_prepare(self, op):
        var = op[1]
        step = self.stack.pop() if self.stack else 1
        end = self.stack.pop() if self.stack else 0
        start = self.stack.pop() if self.stack else 0
        self.env[var] = start
        self.stack.append(start)
        self.stack.append(end)
        self.stack.append(step)
    def _get_property(self, op):
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
    def _get_index(self, op):
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
    def _add(self, op):
        b = self.stack.pop() if self.stack else 0
        a = self.stack.pop() if self.stack else 0
        self.stack.append(a + b)
    def _sub(self, op):
        b = self.stack.pop() if self.stack else 0
        a = self.stack.pop() if self.stack else 0
        self.stack.append(a - b)
    def _mul(self, op):
        b = self.stack.pop() if self.stack else 0
        a = self.stack.pop() if self.stack else 0
        self.stack.append(a * b)
    def _div(self, op):
        b = self.stack.pop() if self.stack else 0
        a = self.stack.pop() if self.stack else 0
        self.stack.append(a / b if b != 0 else 0)
    def _mod(self, op):
        b = self.stack.pop() if self.stack else 0
        a = self.stack.pop() if self.stack else 0
        self.stack.append(a % b if b != 0 else 0)
    def _pow(self, op):
        b = self.stack.pop() if self.stack else 0
        a = self.stack.pop() if self.stack else 0
        self.stack.append(math.pow(a, b))
    def _concat(self, op):
        b = self.stack.pop() if self.stack else ''
        a = self.stack.pop() if self.stack else ''
        self.stack.append(str(a) + str(b))
    def _lt(self, op):
        b = self.stack.pop() if self.stack else 0
        a = self.stack.pop() if self.stack else 0
        self.stack.append(a < b)
    def _le(self, op):
        b = self.stack.pop() if self.stack else 0
        a = self.stack.pop() if self.stack else 0
        self.stack.append(a <= b)
    def _gt(self, op):
        b = self.stack.pop() if self.stack else 0
        a = self.stack.pop() if self.stack else 0
        self.stack.append(a > b)
    def _ge(self, op):
        b = self.stack.pop() if self.stack else 0
        a = self.stack.pop() if self.stack else 0
        self.stack.append(a >= b)
    def _eq(self, op):
        b = self.stack.pop() if self.stack else 0
        a = self.stack.pop() if self.stack else 0
        self.stack.append(a == b)
    def _ne(self, op):
        b = self.stack.pop() if self.stack else 0
        a = self.stack.pop() if self.stack else 0
        self.stack.append(a != b)
    def _and(self, op):
        b = self.stack.pop() if self.stack else False
        a = self.stack.pop() if self.stack else False
        self.stack.append(a and b)
    def _or(self, op):
        b = self.stack.pop() if self.stack else False
        a = self.stack.pop() if self.stack else False
        self.stack.append(a or b)

    def callfunction(self, name, params, args):
        return None
