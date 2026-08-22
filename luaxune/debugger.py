import sys as _sys
import traceback as _traceback

class _debugstate:
    def __init__(self):
        self.breakpoints = set()
        self.stopped = False
        self.watches = {}
        self.stack = []

_debug = _debugstate()

def _breakpoint():
    _debug.stopped = True
    _debug.stack = _traceback.extract_stack()
    print('Breakpoint reached. Use debugger.step() or debugger.continue()')
    while _debug.stopped:
        cmd = input('debug> ')
        if cmd == 'step':
            _debug.stopped = False
        elif cmd == 'continue':
            _debug.stopped = False
            break
        elif cmd == 'inspect':
            var = input('variable: ')
            if var in globals():
                print(globals()[var])
            else:
                print('not found')
        elif cmd == 'stacktrace':
            for line in _debug.stack:
                print(line)
        elif cmd == 'watch':
            expr = input('expression: ')
            try:
                val = eval(expr)
                _debug.watches[expr] = val
                print(val)
            except:
                print('invalid expression')
        elif cmd == 'break':
            line = int(input('line: '))
            _debug.breakpoints.add(line)
        else:
            print('commands: step, continue, inspect, stacktrace, watch, break')

def _step():
    _debug.stopped = False

def _continue():
    _debug.stopped = False

def _inspect(var):
    if var in globals():
        return globals()[var]
    return None

def _stacktrace():
    return _debug.stack

def _watch(expr):
    try:
        val = eval(expr)
        _debug.watches[expr] = val
        return val
    except:
        return None

def _set_breakpoint(line):
    _debug.breakpoints.add(line)

_debuggertable = {
    'breakpoint': _breakpoint,
    'step': _step,
    'continue': _continue,
    'inspect': _inspect,
    'stacktrace': _stacktrace,
    'watch': _watch,
    'set_breakpoint': _set_breakpoint,
      }
