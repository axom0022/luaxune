import math as _math
import random as _random
import re as _re
import time as _time
import datetime as _datetime
import sys as _sys
from .types import _LuauTable, nil

def type_(obj):
    if obj is nil:
        return 'nil'
    if isinstance(obj, bool):
        return 'boolean'
    if isinstance(obj, (int, float)):
        return 'number'
    if isinstance(obj, str):
        return 'string'
    if callable(obj):
        return 'function'
    if isinstance(obj, _LuauTable):
        return 'table'
    return 'userdata'

def tonumber(s, base=10):
    if isinstance(s, (int, float)):
        return s
    if isinstance(s, str):
        try:
            return int(s, base) if base else float(s)
        except:
            return nil
    return nil

def tostring(v):
    if v is nil:
        return 'nil'
    if isinstance(v, bool):
        return str(v).lower()
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return v
    if isinstance(v, _LuauTable):
        return str(v)
    return repr(v)

def rawget(table, key):
    if isinstance(table, _LuauTable):
        return table._rawget(key)
    return nil

def rawset(table, key, value):
    if isinstance(table, _LuauTable):
        table._rawset(key, value)
    else:
        error('rawset on non-table')

def rawlen(table):
    if isinstance(table, _LuauTable):
        return table._rawlen()
    if isinstance(table, (list, tuple, dict)):
        return len(table)
    return 0

def select(index, *args):
    if isinstance(index, str) and index == '#':
        return len(args)
    if isinstance(index, int):
        if index > 0:
            return args[index-1:]
        else:
            return args[index:]
    return nil

def next(table, index=None):
    if not isinstance(table, (_LuauTable, dict)):
        error('table expected')
    keys = list(table._dict.keys()) if isinstance(table, _LuauTable) else list(table.keys())
    if index is None:
        if keys:
            return keys[0], table[keys[0]]
        return nil
    try:
        idx = keys.index(index)
        if idx + 1 < len(keys):
            return keys[idx+1], table[keys[idx+1]]
        return nil
    except ValueError:
        return nil

def pairs(table):
    return next, table, nil

def ipairs(table):
    if not isinstance(table, (_LuauTable, list, tuple)):
        error('table expected')
    if isinstance(table, _LuauTable):
        lst = list(table._dict.values())
    else:
        lst = list(table)
    def _iter(state, i):
        i += 1
        if i <= len(lst):
            return i, lst[i-1]
        return nil
    return _iter, nil, 0

def pcall(func, *args):
    try:
        return True, func(*args)
    except Exception as e:
        return False, str(e)

def xpcall(func, errhandler, *args):
    try:
        return True, func(*args)
    except Exception as e:
        return False, errhandler(e)

def setmetatable(table, metatable):
    if isinstance(table, _LuauTable):
        table._set_metatable(metatable)
        return table
    error('setmetatable on non-table')

def getmetatable(table):
    if isinstance(table, _LuauTable):
        return table._get_metatable()
    return nil
