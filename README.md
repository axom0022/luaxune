# Luaxune Documentation

Luaxune is a Python-based Luau runtime that executes Luau scripts on mobile devices, desktops, or anywhere Python runs. It includes a full parser, bytecode compiler, virtual machine, and the complete Roblox API mock with all services, instances, data types, and global functions.

---

Installation

Luaxune can be used in several ways:

Copy the luaxune folder into your project and import it directly
Install with pip by running pip install . in the directory containing setup.py
Bundle as a zip file for distribution
Package as an exe using PyInstaller after installation

The library has no external dependencies and works on Python 3.7 and above.

---

Quick Start

```python
import luaxune

result = luaxune.execute("""
    local x = 10
    local y = 20
    return x + y
""")
print(result)
```

```python
import luaxune

part = luaxune.Part()
part.Position = luaxune.Vector3(10, 5, 0)
part.Color = luaxune.Color3.from_rgb(255, 0, 0)
print(part.Name, part.Position, part.Color)

model = luaxune.Model()
model.Name = "MyModel"
part.Parent = model
print(model.GetChildren())

game = luaxune.game
player = game.Players.CreatePlayer(12345, "JohnDoe")
print(player.DisplayName)
```

---

Core Functions

execute(code, env=None)

Executes a Luau code string and returns the result.

```python
result = luaxune.execute("return 2 + 2")
```

executefile(path, env=None)

Reads and executes a Luau script file.

```python
result = luaxune.executefile("script.luau")
```

---

Data Types

Vector3

Represents 3D coordinates with x, y, z components.

```python
v1 = luaxune.Vector3(1, 2, 3)
v2 = luaxune.Vector3(4, 5, 6)

print(v1 + v2)
print(v1 * 2)
print(v1.magnitude())
print(v1.unit())
print(v1.dot(v2))
print(v1.cross(v2))
print(v1.lerp(v2, 0.5))
```

Properties and methods:

x, y, z - float components
magnitude() - returns length of vector
unit() - returns normalized vector
dot(other) - dot product
cross(other) - cross product
lerp(other, t) - linear interpolation

CFrame

Represents position and orientation (simplified implementation).

```python
cf = luaxune.CFrame.new(0, 10, 0)
print(cf.position)
point = cf * luaxune.Vector3(1, 0, 0)
```

Static methods:

new(x, y, z) - creates CFrame at position
look_at(pos, target, up) - creates CFrame looking at target

Color3

RGB color with components from 0 to 1.

```python
c = luaxune.Color3(0.5, 0.2, 0.8)
c2 = luaxune.Color3.from_rgb(255, 0, 0)
c3 = luaxune.Color3.from_hsv(0.5, 1, 1)
```

Methods:

from_rgb(r, g, b) - creates Color3 from 0-255 values
from_hsv(h, s, v) - creates Color3 from HSV (simplified)

Rect

Rectangle with x0, y0, x1, y1 coordinates.

```python
rect = luaxune.Rect(0, 0, 100, 200)
```

UDim

Scale and offset for UI positioning.

```python
udim = luaxune.UDim(0.5, 10)
```

UDim2

Combination of two UDim for x and y dimensions.

```python
udim2 = luaxune.UDim2(0.5, 10, 0.2, 5)
```

nil

The nil value represents nothing or no value.

```python
if result is luaxune.nil:
    print("Value is nil")
```

---

Standard Libraries

math

All standard math functions and constants.

```python
luaxune.math.pi
luaxune.math.abs(-5)
luaxune.math.random()
luaxune.math.randomseed(42)
luaxune.math.sin(1.0)
luaxune.math.cos(1.0)
luaxune.math.tan(1.0)
luaxune.math.sqrt(16)
luaxune.math.pow(2, 3)
luaxune.math.log(10)
luaxune.math.ceil(3.14)
luaxune.math.floor(3.14)
luaxune.math.max(1, 2, 3)
luaxune.math.min(1, 2, 3)
```

string

String manipulation functions.

```python
s = "Hello, World!"
luaxune.string.len(s)
luaxune.string.sub(s, 1, 5)
luaxune.string.upper(s)
luaxune.string.lower(s)
luaxune.string.reverse(s)
luaxune.string.rep(s, 3)
luaxune.string.find(s, "Wor")
luaxune.string.gsub(s, "o", "0")
luaxune.string.gmatch(s, "%a+")
luaxune.string.match(s, "Hello")
luaxune.string.format("%s %d", "Value", 42)
luaxune.string.byte(s, 1)
luaxune.string.char(72, 101, 108, 108, 111)
```

table

Table manipulation functions.

```python
t = luaxune.table.pack(1, 2, 3)
luaxune.table.concat(t, ", ")
luaxune.table.insert(t, 2, 99)
luaxune.table.remove(t, 2)
luaxune.table.sort(t)
luaxune.table.unpack(t)
```

os

Operating system functions (mocked).

```python
luaxune.os.time()
luaxune.os.date("%Y-%m-%d")
luaxune.os.clock()
luaxune.os.difftime(t1, t2)
```

coroutine

Coroutine functions (simplified).

```python
co = luaxune.coroutine.create(lambda x: x * 2)
success, result = luaxune.coroutine.resume(co, 5)
luaxune.coroutine.yield(42)
luaxune.coroutine.status(co)
luaxune.coroutine.wrap(lambda x: x * 2)
luaxune.coroutine.running()
```

debug

Debugging functions.

```python
luaxune.debug.traceback()
luaxune.debug.getinfo(1)
```

---

Global Functions

print(*args, sep=' ', end='\n')

Prints to stdout.

warn(*args)

Prints to stderr with "Warning:" prefix.

error(msg, level=1)

Raises a RuntimeError.

assert(cond, msg=None)

Raises error if condition is false.

type(obj)

Returns type name as string: "nil", "boolean", "number", "string", "function", "table", "userdata".

tonumber(s, base=10)

Converts string to number, returns nil on failure.

tostring(v)

Converts value to string.

rawget(table, key)

Gets value from table without metatable.

rawset(table, key, value)

Sets value in table without metatable.

rawlen(table)

Gets length of table without metatable.

select(index, *args)

Returns arguments from index or count if index is "#".

next(table, index=None)

Returns next key-value pair for iteration.

pairs(table)

Returns iterator for table key-value pairs.

ipairs(table)

Returns iterator for table array part.

pcall(func, *args)

Calls function with error handling, returns success and result.

xpcall(func, errhandler, *args)

Calls function with custom error handler.

setmetatable(table, metatable)

Sets metatable for table.

getmetatable(table)

Gets metatable of table.

---

Instance System

Instance

Base class for all Roblox objects.

Properties:

Name - string, read/write
ClassName - string, read-only
Parent - Instance or nil, read/write

Methods:

GetFullName() - returns full path name
FindFirstChild(name, recursive=False) - returns child or nil
WaitForChild(name, timeout=None) - waits for child to appear
GetChildren() - returns list of immediate children
GetDescendants() - returns list of all descendants
IsA(class_name) - checks if instance is of given class
Clone(parent=None) - creates a deep copy
Destroy() - removes from parent and clears children
AddTag(tag) - adds a tag
HasTag(tag) - checks if tag exists
RemoveTag(tag) - removes a tag
GetTags() - returns list of tags
GetAttribute(attr) - gets custom attribute
SetAttribute(attr, value) - sets custom attribute
GetAttributes() - returns all attributes
ClearAttributes() - removes all attributes
GetDebugId() - returns hex id
GetDebugChildren() - returns debug children
GetDebugString() - returns debug string

Events:

Changed - fires when Name changes
AncestryChanged - fires when Parent changes
ChildAdded - fires when child is added
ChildRemoved - fires when child is removed
DescendantAdded - fires when descendant is added
DescendantRemoved - fires when descendant is removed
PropertyChanged - fires when attribute changes

Part

3D physical object extending Instance.

Properties:

Size - Vector3
Position - Vector3
Orientation - Vector3
Color - Color3
Material - string ("Plastic", "Metal", etc.)
Transparency - float 0-1
Reflectance - float 0-1
Anchored - boolean
CanCollide - boolean
Velocity - Vector3
RotVelocity - Vector3

Model

Container for parts extending Instance.

Methods:

GetPrimaryPart() - returns primary Part or nil
SetPrimaryPart(part) - sets the primary part

Tool

Tool object extending Instance.

Properties:

CanEquip - boolean
RequiresHandle - boolean
Grip - CFrame

Methods:

Equip(player) - equips tool
Unequip() - unequips tool
Activate() - activates tool

Player

Player object extending Instance.

Properties:

UserId - int
DisplayName - string
AccountAge - int
Character - Model or nil

Methods:

LoadCharacter() - loads character

Folder

Simple container extending Instance.

---

Services

All services are available as children of the global game object.

Players

Player management service.

Methods:

GetPlayers() - returns list of all players
GetPlayerByUserId(id) - returns player or nil
GetPlayerByName(name) - returns player or nil
CreatePlayer(user_id, name) - creates and adds a player

DataStoreService

Data storage service.

Methods:

GetDataStore(name, scope=None) - returns a data store table

HttpService

HTTP request service.

Properties:

HttpEnabled - boolean

Methods:

GetAsync(url, headers=None) - returns mock JSON string
PostAsync(url, data, content_type) - returns mock JSON string
RequestAsync(options) - returns mock response
JSONDecode(data) - decodes JSON using Python json
JSONEncode(data) - encodes JSON using Python json

TweenService

Animation service.

Methods:

Create(instance, tween_info, properties) - returns mock tween object
GetTweenInfo(duration, easing_style, easing_direction, repeat_count=0, reverses=False, delay_time=0) - returns tween info table

RunService

Game loop service.

Properties:

Heartbeat - Event
Stepped - Event
RenderStepped - Event

Methods:

IsServer() - returns True
IsClient() - returns False
IsStudio() - returns False

Lighting

Environment lighting service.

Properties:

Brightness - float
ClockTime - float (0-24 hours)
Ambient - Color3

SoundService

Audio service.

Properties:

Volume - float
DistanceFactor - float

UserInputService

Input handling service.

Properties:

MouseEnabled - boolean
MouseBehaviour - string

ContextActionService

Action binding service.

Methods:

BindAction(action_name, callback, create_button=True, touch_screen_controls=None)
UnbindAction(action_name)

MarketplaceService

Purchase service.

Methods:

CanPurchase(player, product_id) - returns True
PurchaseProduct(player, product_id) - returns True

TeleportService

Teleport service.

Methods:

Teleport(place_id, players, options=None)

GuiService

GUI service.

Methods:

GetGuiInset() - returns Rect

TextService

Text filtering service.

Methods:

FilterAsync(text, from_user_id, context) - returns same text

PathfindingService

Pathfinding service.

Methods:

CreatePath(options=None) - returns mock path object with ComputeAsync, GetWaypoints, IsBlocked

CollectionService

Tag management service.

Methods:

AddTag(instance, tag)
RemoveTag(instance, tag)
HasTag(instance, tag) - returns boolean
GetTagged(tag) - returns list of instances
GetTags(instance) - returns list of tags
IsInstanceInTag(instance, tag) - returns boolean

ReplicatedStorage

Storage for replicated objects extending Instance.

ServerStorage

Storage for server-only objects extending Instance.

ServerScriptService

Container for server scripts extending Instance.

StarterGui

Container for GUI objects extending Instance.

StarterPack

Container for starter tools extending Instance.

StarterPlayer

Starter player settings extending Instance.

---

Events

Events are used for callbacks and signals.

Event

Methods:

connect(callback) - registers a callback, returns disconnect function
fire(*args) - calls all connected callbacks

```python
event = luaxune._Event()
event.connect(lambda x: print("Got", x))
event.fire(42)
connection = event.connect(func)
connection()
```

---

Enums

Enum

Enumeration container.

```python
enum = luaxune.Enum("MyEnum", {"One": 1, "Two": 2})
print(enum.One)
print(enum["Two"])
for item in enum:
    print(item.name, item.value)
```

EnumItem

Individual enumeration item.

Properties:

name - string
value - int

---

The Game Object

The global game object is a pre-configured Instance containing all services as children.

```python
game = luaxune.game
print(game.Players)
print(game.Lighting)
print(game.ReplicatedStorage)
print(game.ServerStorage)
print(game.RunService)
print(game.DataStoreService)
```

---

Metatables

Luau tables support metatables for custom behavior.

```python
t = luaxune._LuauTable()
mt = luaxune._LuauTable()
mt["__index"] = lambda self, key: "default"
luaxune.setmetatable(t, mt)
print(t["foo"])
```

Supported metamethods:

__index - table lookup fallback
__newindex - table assignment fallback
__call - function call on table
__add, __sub, __mul, __div, __mod, __pow - arithmetic operators
__unm - unary minus
__eq, __lt, __le - comparison operators
__len - length operator
__tostring - string conversion

---

Example Scripts

Basic arithmetic

```python
import luaxune
result = luaxune.execute("""
    local x = 10
    local y = 20
    return x + y
""")
print(result)
```

Using tables and functions

```python
import luaxune
result = luaxune.execute("""
    local t = {1, 2, 3}
    local function sum(t)
        local s = 0
        for i, v in ipairs(t) do
            s = s + v
        end
        return s
    end
    return sum(t)
""")
print(result)
```

Creating parts and models

```python
import luaxune

code = """
    local part = Instance.new("Part")
    part.Name = "MyPart"
    part.Position = Vector3.new(10, 5, 0)
    part.Color = Color3.from_rgb(255, 0, 0)
    
    local model = Instance.new("Model")
    model.Name = "MyModel"
    part.Parent = model
    
    return model:GetChildren()
"""
result = luaxune.execute(code)
print(result)
```

Using services

```python
import luaxune

code = """
    local game = game
    local players = game:FindFirstChild("Players")
    local player = players:CreatePlayer(12345, "JohnDoe")
    return player.DisplayName
"""
result = luaxune.execute(code)
print(result)
```

Event handling

```python
import luaxune

code = """
    local part = Instance.new("Part")
    local count = 0
    part.Changed:connect(function(prop, old, new)
        count = count + 1
    end)
    part.Name = "NewName"
    part.Name = "AnotherName"
    return count
"""
result = luaxune.execute(code)
print(result)
```

---

Mobile Support

Luaxune is pure Python with no binary dependencies and runs on:

Android via Termux (install Python then pip install .)
iOS via Pythonista or a-Shell
Any Python 3.7+ interpreter

All features work identically on mobile devices.

---

Limitations

unfinished networking - HTTP requests return dummy data cuz it's not finished
Simplified CFrame - only position and basic multiplication (it'll get improved dw) 
TweenService returns mock objects only (also unfinished) 
DataStoreService stores data in memory, not persistent 
All services are synchronous with no async/aawai (cuz this is still v1 yk) 

Version : V1
