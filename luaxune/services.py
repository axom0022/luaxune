from .instances import Instance, Player
from .types import _LuauTable, Vector3, Color3, Rect, nil
from .events import _Event

class Service(Instance):
    def __init__(self, name):
        super().__init__(name)

class DataStoreService(Service):
    def __init__(self):
        super().__init__('DataStoreService')
        self._stores = {}
    def GetDataStore(self, name, scope=None):
        if name not in self._stores:
            self._stores[name] = _LuauTable({})
        return self._stores[name]

class Players(Service):
    def __init__(self):
        super().__init__('Players')
        self._players = []
    def GetPlayers(self):
        return self._players
    def GetPlayerByUserId(self, id):
        for p in self._players:
            if p.UserId == id:
                return p
        return nil
    def GetPlayerByName(self, name):
        for p in self._players:
            if p.DisplayName == name:
                return p
        return nil
    def CreatePlayer(self, user_id, name):
        p = Player()
        p.UserId = user_id
        p.DisplayName = name
        self._players.append(p)
        return p

class ReplicatedStorage(Instance):
    def __init__(self):
        super().__init__('ReplicatedStorage')

class ServerStorage(Instance):
    def __init__(self):
        super().__init__('ServerStorage')

class ServerScriptService(Instance):
    def __init__(self):
        super().__init__('ServerScriptService')

class StarterGui(Instance):
    def __init__(self):
        super().__init__('StarterGui')

class StarterPack(Instance):
    def __init__(self):
        super().__init__('StarterPack')

class StarterPlayer(Instance):
    def __init__(self):
        super().__init__('StarterPlayer')

class Lighting(Instance):
    def __init__(self):
        super().__init__('Lighting')
        self._brightness = 1
        self._clock_time = 12
        self._ambient = Color3(0.5,0.5,0.5)
        self._color_correction = nil
    @property
    def Brightness(self):
        return self._brightness
    @Brightness.setter
    def Brightness(self, v):
        self._brightness = v
    @property
    def ClockTime(self):
        return self._clock_time
    @ClockTime.setter
    def ClockTime(self, v):
        self._clock_time = v
    @property
    def Ambient(self):
        return self._ambient
    @Ambient.setter
    def Ambient(self, c):
        self._ambient = c

class SoundService(Instance):
    def __init__(self):
        super().__init__('SoundService')
        self._volume = 1
        self._distance_factor = 1
    @property
    def Volume(self):
        return self._volume
    @Volume.setter
    def Volume(self, v):
        self._volume = v
    @property
    def DistanceFactor(self):
        return self._distance_factor
    @DistanceFactor.setter
    def DistanceFactor(self, v):
        self._distance_factor = v

class HttpService(Service):
    def __init__(self):
        super().__init__('HttpService')
        self._http_enabled = False
    @property
    def HttpEnabled(self):
        return self._http_enabled
    @HttpEnabled.setter
    def HttpEnabled(self, b):
        self._http_enabled = b
    def GetAsync(self, url, headers=None):
        return '{}'
    def PostAsync(self, url, data, content_type='application/json'):
        return '{}'
    def RequestAsync(self, options):
        return {'Body': '{}', 'Headers': {}, 'StatusCode': 200}
    def JSONDecode(self, data):
        import json
        return json.loads(data)
    def JSONEncode(self, data):
        import json
        return json.dumps(data)

class TweenService(Service):
    def __init__(self):
        super().__init__('TweenService')
    def Create(self, instance, tween_info, properties):
        return _LuauTable({'play': lambda: nil, 'cancel': lambda: nil, 'stop': lambda: nil, 'destroy': lambda: nil})
    def GetTweenInfo(self, duration, easing_style, easing_direction, repeat_count=0, reverses=False, delay_time=0):
        return _LuauTable({
            'Duration': duration,
            'EasingStyle': easing_style,
            'EasingDirection': easing_direction,
            'RepeatCount': repeat_count,
            'Reverses': reverses,
            'DelayTime': delay_time,
        })

class RunService(Service):
    def __init__(self):
        super().__init__('RunService')
        self._heartbeat = _Event()
        self._stepped = _Event()
        self._render_stepped = _Event()
    @property
    def Heartbeat(self):
        return self._heartbeat
    @property
    def Stepped(self):
        return self._stepped
    @property
    def RenderStepped(self):
        return self._render_stepped
    def IsServer(self):
        return True
    def IsClient(self):
        return False
    def IsStudio(self):
        return False

class UserInputService(Service):
    def __init__(self):
        super().__init__('UserInputService')
        self._mouse_enabled = True
        self._mouse_behaviour = 'Default'
    @property
    def MouseEnabled(self):
        return self._mouse_enabled
    @MouseEnabled.setter
    def MouseEnabled(self, b):
        self._mouse_enabled = b
    @property
    def MouseBehaviour(self):
        return self._mouse_behaviour
    @MouseBehaviour.setter
    def MouseBehaviour(self, s):
        self._mouse_behaviour = s

class ContextActionService(Service):
    def __init__(self):
        super().__init__('ContextActionService')
    def BindAction(self, action_name, callback, create_button=True, touch_screen_controls=nil):
        pass
    def UnbindAction(self, action_name):
        pass

class MarketplaceService(Service):
    def __init__(self):
        super().__init__('MarketplaceService')
    def CanPurchase(self, player, product_id):
        return True
    def PurchaseProduct(self, player, product_id):
        return True

class TeleportService(Service):
    def __init__(self):
        super().__init__('TeleportService')
    def Teleport(self, place_id, players, options=None):
        pass

class GuiService(Service):
    def __init__(self):
        super().__init__('GuiService')
    def GetGuiInset(self):
        return Rect(0,0,0,0)

class TextService(Service):
    def __init__(self):
        super().__init__('TextService')
    def FilterAsync(self, text, from_user_id, context):
        return text

class PathfindingService(Service):
    def __init__(self):
        super().__init__('PathfindingService')
    def CreatePath(self, options=None):
        return _LuauTable({
            'ComputeAsync': lambda start, end: False,
            'GetWaypoints': lambda: [],
            'IsBlocked': lambda: False,
        })

class CollectionService(Service):
    def __init__(self):
        super().__init__('CollectionService')
        self._tags = {}
    def AddTag(self, instance, tag):
        if tag not in self._tags:
            self._tags[tag] = []
        self._tags[tag].append(instance)
        instance.AddTag(tag)
    def RemoveTag(self, instance, tag):
        if tag in self._tags:
            self._tags[tag] = [inst for inst in self._tags[tag] if inst is not instance]
        instance.RemoveTag(tag)
    def HasTag(self, instance, tag):
        return instance.HasTag(tag)
    def GetTagged(self, tag):
        return self._tags.get(tag, [])
    def GetTags(self, instance):
        return instance.GetTags()
    def IsInstanceInTag(self, instance, tag):
        return instance.HasTag(tag)
