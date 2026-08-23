from .types import *
from .instances import *
from .services import *
from .events import *
from .enums import *
from .standard import standardlibrary
from .io import _iotable
from .http import _httptable
from .debugger import _debuggertable
from .logger import _loggertable
from .profile import _profiletable
from .core import type_, tonumber, tostring, rawget, rawset, rawlen, select, next, pairs, ipairs, pcall, xpcall, setmetatable, getmetatable
from .globals import print_, warn, error

def createapi():
    api = {
        'globals': {},
        'Vector3': Vector3,
        'CFrame': CFrame,
        'Color3': Color3,
        'Rect': Rect,
        'UDim': UDim,
        'UDim2': UDim2,
        'Instance': Instance,
        'Part': Part,
        'Model': Model,
        'Tool': Tool,
        'Player': Player,
        'Folder': Folder,
        'Enum': Enum,
        'nil': None,
        'print': print_,
        'warn': warn,
        'error': error,
        'type': type_,
        'tonumber': tonumber,
        'tostring': tostring,
        'pcall': pcall,
        'xpcall': xpcall,
        'rawget': rawget,
        'rawset': rawset,
        'rawlen': rawlen,
        'setmetatable': setmetatable,
        'getmetatable': getmetatable,
        'select': select,
        'next': next,
        'pairs': pairs,
        'ipairs': ipairs,
    }

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

    api['game'] = game

    std = standardlibrary()
    api.update(std.getlibraries())

    api['io'] = _iotable
    api['http'] = _httptable
    api['debugger'] = _debuggertable
    api['logger'] = _loggertable
    api['profile'] = _profiletable

    return type('LuauAPI', (), {'globals': api})()
