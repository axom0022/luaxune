from .runtime import luau runtime
from .api import createapi
from .types import *
from .instances import *
from .services import *
from .events import *
from .enums import *

def execute(code, env=None):
    rt = luaruntime()
    return rt.execute(code, env)

def executefile(path, env=None):
    rt = luaruntime()
    return rt.executefile(path, env)

__version__ = "1.0.0"
