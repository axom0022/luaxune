import sys as _sys
import time as _time

from .core import *
from .types import nil
from .instances import Instance, Folder, Part, Model, Tool, Player
from .services import *
from .enums import Enum
from .io import _iotable
from .http import _httptable
from .debugger import _debuggertable
from .logger import _loggertable
from .profile import _profiletable

def print_(*args, sep=' ', end='\n'):
    _sys.stdout.write(sep.join(str(a) for a in args) + end)

def warn(*args):
    _sys.stderr.write('Warning: ' + ' '.join(str(a) for a in args) + '\n')

def error(msg, level=1):
    raise RuntimeError(str(msg))

def assert_(cond, msg=None):
    if not cond:
        error(msg or 'assertion failed!')
    return cond

game = Instance('DataModel')
game.ReplicatedStorage = ReplicatedStorage()
game.ReplicatedStorage.Parent = game
game.ServerStorage = ServerStorage()
game.ServerStorage.Parent = game
game.ServerScriptService = ServerScriptService()
game.ServerScriptService.Parent = game
game.StarterGui = StarterGui()
game.StarterGui.Parent = game
game.StarterPack = StarterPack()
game.StarterPack.Parent = game
game.StarterPlayer = StarterPlayer()
game.StarterPlayer.Parent = game
game.Lighting = Lighting()
game.Lighting.Parent = game
game.SoundService = SoundService()
game.SoundService.Parent = game
game.Players = Players()
game.Players.Parent = game
game.DataStoreService = DataStoreService()
game.DataStoreService.Parent = game
game.HttpService = HttpService()
game.HttpService.Parent = game
game.TweenService = TweenService()
game.TweenService.Parent = game
game.RunService = RunService()
game.RunService.Parent = game
game.UserInputService = UserInputService()
game.UserInputService.Parent = game
game.ContextActionService = ContextActionService()
game.ContextActionService.Parent = game
game.MarketplaceService = MarketplaceService()
game.MarketplaceService.Parent = game
game.TeleportService = TeleportService()
game.TeleportService.Parent = game
game.GuiService = GuiService()
game.GuiService.Parent = game
game.TextService = TextService()
game.TextService.Parent = game
game.PathfindingService = PathfindingService()
game.PathfindingService.Parent = game
game.CollectionService = CollectionService()
game.CollectionService.Parent = game

print = print_
type = type_
