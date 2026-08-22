import math as _math
import random as _random
import re as _re
import time as _time
import datetime as _datetime
import sys as _sys
from .types import _LuauTable, nil

def type_(obj):
    if obj is nil: return "nil"
    if isinstance(obj, bool): return "boolean"
    if isinstance(obj, (int, float)): return "number"
    if isinstance(obj, str): return "string"
    if callable(obj): return "function"
    if isinstance(obj, _LuauTable): return "table"
    return "userdata"

def tonumber(s, base=10):
    if isinstance(s, (int, float)): return s
    if isinstance(s, str):
        try: return int(s, base) if base else float(s)
        except: return nil
    return nil

def tostring(v):
    if v is nil: return "nil"
    if isinstance(v, bool): return str(v).lower()
    if isinstance(v, (int, float)): return str(v)
    if isinstance(v, str): return v
    if isinstance(v, _LuauTable): return str(v)
    return repr(v)

def rawget(table, key):
    if isinstance(table, _LuauTable): return table._rawget(key)
    return nil

def rawset(table, key, value):
    if isinstance(table, _LuauTable): table._rawset(key, value)
    else: error("rawset on non-table")

def rawlen(table):
    if isinstance(table, _LuauTable): return table._rawlen()
    if isinstance(table, (list, tuple, dict)): return len(table)
    return 0

def select(index, *args):
    if isinstance(index, str) and index == "#": return len(args)
    if isinstance(index, int):
        if index > 0: return args[index-1:]
        else: return args[index:]
    return nil

def next(table, index=None):
    if not isinstance(table, (_LuauTable, dict)): error("table expected")
    keys = list(table._dict.keys()) if isinstance(table, _LuauTable) else list(table.keys())
    if index is None:
        if keys: return keys[0], table[keys[0]]
        return nil
    try:
        idx = keys.index(index)
        if idx + 1 < len(keys): return keys[idx+1], table[keys[idx+1]]
        return nil
    except ValueError: return nil

def pairs(table):
    return next, table, nil

def ipairs(table):
    if not isinstance(table, (_LuauTable, list, tuple)): error("table expected")
    if isinstance(table, _LuauTable): lst = list(table._dict.values())
    else: lst = list(table)
    def _iter(state, i):
        i += 1
        if i <= len(lst): return i, lst[i-1]
        return nil
    return _iter, nil, 0

def pcall(func, *args):
    try: return True, func(*args)
    except Exception as e: return False, str(e)

def xpcall(func, errhandler, *args):
    try: return True, func(*args)
    except Exception as e: return False, errhandler(e)

def setmetatable(table, metatable):
    if isinstance(table, _LuauTable):
        table._set_metatable(metatable)
        return table
    error("setmetatable on non-table")

def getmetatable(table):
    if isinstance(table, _LuauTable): return table._get_metatable()
    return nil

math = _LuauTable({
    "pi": _math.pi, "huge": float("inf"),
    "abs": _math.fabs, "acos": _math.acos, "asin": _math.asin,
    "atan": _math.atan, "atan2": _math.atan2, "ceil": _math.ceil,
    "cos": _math.cos, "cosh": _math.cosh, "deg": _math.degrees,
    "exp": _math.exp, "floor": _math.floor, "fmod": _math.fmod,
    "frexp": _math.frexp, "ldexp": _math.ldexp, "log": _math.log,
    "log10": _math.log10, "max": max, "min": min,
    "modf": _math.modf, "pow": _math.pow, "rad": _math.radians,
    "random": _random.random, "randomseed": _random.seed,
    "sin": _math.sin, "sinh": _math.sinh, "sqrt": _math.sqrt,
    "tan": _math.tan, "tanh": _math.tanh,
})

string = _LuauTable({
    "byte": lambda s, i=1, j=None: [ord(c) for c in s[i-1:j]] if j else ord(s[i-1]),
    "char": lambda *args: "".join(chr(a) for a in args),
    "find": lambda s, pattern, init=1, plain=False: (s.find(pattern, init-1) + 1 if s.find(pattern, init-1) is not None else nil,),
    "format": lambda fmt, *args: fmt % args,
    "gmatch": lambda s, pattern: (m for m in _re.findall(pattern, s)),
    "gsub": lambda s, pattern, repl, n=None: (s.replace(pattern, repl, n) if n else s.replace(pattern, repl), 0),
    "len": len, "lower": str.lower,
    "match": lambda s, pattern, init=1: s.find(pattern, init-1) is not None,
    "rep": lambda s, n: s * n, "reverse": lambda s: s[::-1],
    "sub": lambda s, i, j=None: s[i-1:j], "upper": str.upper,
})

table = _LuauTable({
    "insert": lambda t, pos, val: t._dict.__setitem__(pos, val) if isinstance(t, _LuauTable) else t.insert(pos, val),
    "remove": lambda t, pos: t._dict.pop(pos, nil) if isinstance(t, _LuauTable) else t.pop(pos-1),
    "sort": lambda t, comp=None: (t._dict.__setitem__(i, v) for i, v in enumerate(sorted(t._dict.values(), key=lambda x: x if comp is None else comp), 1)) if isinstance(t, _LuauTable) else t.sort(key=comp),
    "concat": lambda t, sep="", i=1, j=None: sep.join(str(v) for v in (list(t._dict.values()) if isinstance(t, _LuauTable) else t)[i-1:j]),
    "pack": lambda *args: _LuauTable({i+1: v for i, v in enumerate(args)}),
    "unpack": lambda t, i=1, j=None: tuple((t._dict.get(k) if isinstance(t, _LuauTable) else t[k-1]) for k in range(i, (j or len(t))+1)),
})

os = _LuauTable({
    "clock": _time.process_time,
    "date": lambda fmt=None, time=None: _datetime.datetime.fromtimestamp(time or _time.time()).strftime(fmt or "%c"),
    "time": _time.time,
    "difftime": _time.time.__sub__,
    "execute": lambda cmd: 0,
})

coroutine = _LuauTable({
    "create": lambda f: f,
    "resume": lambda co, *args: (True, co(*args) if callable(co) else nil),
    "yield": lambda *args: (args[0] if len(args)==1 else args),
    "status": lambda co: "dead",
    "wrap": lambda f: lambda *args: f(*args),
    "running": lambda: (nil, False),
})

debug = _LuauTable({
    "traceback": lambda msg=None, level=1: _sys.exc_info()[2] if msg is None else msg,
    "getinfo": lambda level, options=None: _LuauTable({
        "name": "", "what": "C", "source": "", "short_src": "",
        "linedefined": 0, "lastlinedefined": 0, "nups": 0, "nparams": 0,
        "isvararg": False, "currentline": 0, "func": nil,
    }),
})
