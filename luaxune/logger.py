import sys as _sys
import ast as _ast
import builtins as _builtins

class _logger:
    def __init__(self):
        self.active = False
        self.logs = []
        self.trace = []
        self.env = {}

    def start(self):
        self.active = True
        self.logs = []
        self.trace = []
        self.env = {}
        _builtins._log = self._log

    def stop(self):
        self.active = False
        if hasattr(_builtins, '_log'):
            del _builtins._log

    def _log(self, event, *args):
        if self.active:
            self.logs.append((event, args))
            self.trace.append(event)

    def dump(self):
        return self.logs

    def trace(self):
        return self.trace

    def deobfuscate(self, script):
        self.start()
        try:
            exec(script, {}, self.env)
        except:
            pass
        self.stop()
        readable = []
        for event, args in self.logs:
            if event == 'assign':
                var, val = args
                readable.append(f'{var} = {val}')
            elif event == 'call':
                func, args = args
                readable.append(f'{func}({", ".join(str(a) for a in args)})')
            elif event == 'return':
                val = args[0]
                readable.append(f'return {val}')
            elif event == 'if':
                cond = args[0]
                readable.append(f'if {cond}')
            elif event == 'loop':
                readable.append('loop')
            else:
                readable.append(str(args))
        return '\n'.join(readable)

_logger_obj = _logger()

_loggertable = {
    'start': _logger_obj.start,
    'stop': _logger_obj.stop,
    'dump': _logger_obj.dump,
    'trace': _logger_obj.trace,
    'deobfuscate': _logger_obj.deobfuscate,
}
