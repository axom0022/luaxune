from .runtime import LuauRuntime
from .api import *
from .datatypes import *
from .instances import *
from .services import *
from .events import *
from .enums import *

def execute(code, env=None):
    runtime = LuauRuntime()
    return runtime.execute(code, env)

def execute_file(path, env=None):
    runtime = LuauRuntime()
    return runtime.execute_file(path, env)

__version__ = "1.0.0"
