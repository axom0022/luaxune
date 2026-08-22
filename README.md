
# Luaxune – Full Roblox Luau for Python

**Luaxune** is a pure-Python library that replicates the entire Roblox Luau API, including all standard libraries (`math`, `string`, `table`, …), data types (`Vector3`, `CFrame`, `Color3`, …), the complete `Instance` hierarchy (`Part`, `Model`, `Tool`, `Player`, …), all Roblox services (`DataStoreService`, `Players`, `RunService`, …), and an event system.  
It is designed to run on **any Python 3.7+ environment**, including **mobile** (Termux, PyDroid, etc.). and desktop/pc

The library is a **full mock** – no external dependencies, everything is implemented in Python. It uses **snake_case** for all internal identifiers (variables, helper functions, private attributes) but the **public API** follows Roblox conventions (PascalCase for classes, camelCase for properties and methods).

---

## Installation

### As a folder
Copy the `luaxune/` directory into your project and import it:

```
import luaxune
```

As a pip package

Run in the directory containing setup.py:

```
pip install .
```

Then you can import luaxune from anywhere.

As a .zip

Compress the entire project folder (including luaxune/ and setup.py). Extract and use as above.

As a standalone .exe

Use PyInstaller to bundle your Python script with the library:

```
pip install pyinstaller
pyinstaller --onefile thescript.py
```

The library will be included automatically.

---

Getting Started

```
import luaxune

# Create a Part
part = luaxune.Part()
part.Name = "MyPart"
part.Position = luaxune.Vector3(10, 5, 0)
part.Color = luaxune.Color3.from_rgb(255, 0, 0)

print(part.Name)                 # "MyPart"
print(part.Position)             # Vector3(10.0, 5.0, 0.0)
print(part.Color)                # Color3(1.0, 0.0, 0.0)

# Model with children
model = luaxune.Model()
model.Name = "MyModel"
part.Parent = model
print(model.GetChildren())       # [Part('MyPart')]

# Access the global game object
game = luaxune.game
player = game.Players.CreatePlayer(12345, "JohnDoe")
print(player.DisplayName)        # "JohnDoe"
```

---

Lua Standard Library

Luaxune provides the complete set of Lua standard libraries as Python objects.

math table

All functions from Lua's math library:

```
luaxune.math.pi                # 3.141592653589793
luaxune.math.abs(-5)           # 5.0
luaxune.math.random()          # random float [0,1)
luaxune.math.randomseed(42)    # seed
```

string table

String manipulation functions:

```
s = "Hello, World!"
luaxune.string.len(s)          # 13
luaxune.string.sub(s, 1, 5)    # "Hello"
luaxune.string.upper(s)        # "HELLO, WORLD!"
luaxune.string.gsub(s, "o", "0")  # ("Hell0, W0rld!", 2)
luaxune.string.find(s, "Wor")  # (8, 10)
```

table table

Table utilities:

```
t = luaxune.table.pack(1, 2, 3)  # returns LuauTable
luaxune.table.concat(t, ", ")    # "1, 2, 3"
luaxune.table.insert(t, 2, 99)   # t becomes {1, 99, 2, 3}
luaxune.table.remove(t, 2)       # removes 99
```

os table

Basic OS functions (mocked where needed):

```
luaxune.os.time()              # current timestamp
luaxune.os.date("%Y-%m-%d")    # "2026-08-22"
luaxune.os.clock()             # CPU time
```

coroutine table

Coroutine functions (simplified):

```
co = luaxune.coroutine.create(lambda x: x*2)
success, res = luaxune.coroutine.resume(co, 5)
print(res)  # 10
```

debug table

Debugging helpers:

```
luaxune.debug.traceback()      # current traceback
luaxune.debug.getinfo(1)       # info table
```

Global functions

```
luaxune.print("Hello")          # print to stdout
luaxune.type(123)               # "number"
luaxune.tonumber("3.14")        # 3.14
luaxune.tostring(nil)           # "nil"
luaxune.error("Something went wrong")
luaxune.assert(1 == 1, "fail")
luaxune.pcall(safe_func, arg)   # (True, result) or (False, error_msg)
luaxune.xpcall(func, err_handler, arg)
luaxune.setmetatable(t, mt)     # set metatable
luaxune.getmetatable(t)         # get metatable
luaxune.rawget(t, key)          # bypass metatable
luaxune.rawset(t, key, val)
luaxune.rawlen(t)               # length ignoring metamethods
luaxune.select("#", 1,2,3)      # returns 3
luaxune.next(t, nil)            # returns first key,value
```

---

Data Types

Vector3

Represents 3D vectors.

```
v1 = luaxune.Vector3(1, 2, 3)
v2 = luaxune.Vector3(4, 5, 6)
print(v1 + v2)          # Vector3(5.0, 7.0, 9.0)
print(v1 * 2)           # Vector3(2.0, 4.0, 6.0)
print(v1.magnitude())   # 3.7416573867739413
print(v1.unit())        # normalized vector
print(v1.dot(v2))       # 32
print(v1.cross(v2))     # Vector3(-3.0, 6.0, -3.0)
print(v1.lerp(v2, 0.5)) # Vector3(2.5, 3.5, 4.5)
```

CFrame

Represents position and rotation (simplified).

```
cf = luaxune.CFrame.new(0, 10, 0)
print(cf.position)      # Vector3(0.0, 10.0, 0.0)
# Multiplication with Vector3 applies transformation (simplified)
point = cf * luaxune.Vector3(1,0,0)
```

Color3

RGB color.

```
c = luaxune.Color3(0.5, 0.2, 0.8)
c2 = luaxune.Color3.from_rgb(255, 0, 0)   # red
c3 = luaxune.Color3.from_hsv(0.5, 1, 1)   # HSV conversion (approximate)
print(c.to_hex())       # "#8033cc"
```

Rect, UDim, UDim2

GUI layout helpers.

```
rect = luaxune.Rect(0, 0, 100, 200)
udim = luaxune.UDim(0.5, 10)          # scale + offset
udim2 = luaxune.UDim2(0.5, 10, 0.2, 5)
```

---

Instances and the Data Model

Luaxune implements the complete Roblox Instance hierarchy.

Instance – base class

All properties and methods that every instance has:

- Name – string, get/set
- ClassName – read‑only
- Parent – get/set
- GetFullName() – returns path like "Workspace.Part"
- FindFirstChild(name, recursive=False) – returns child or nil
- WaitForChild(name, timeout=None) – blocks until child exists
- GetChildren() – list of immediate children
- GetDescendants() – list of all descendants
- IsA(class_name) – boolean
- Clone(parent=None) – deep copy
- Destroy() – removes from parent
- AddTag(tag), HasTag(tag), RemoveTag(tag), GetTags() – tagging system
- GetAttribute(attr), SetAttribute(attr, value), GetAttributes(), ClearAttributes() – custom attributes
- Changed – _Event fired when Name changes
- AncestryChanged – _Event fired when Parent changes

Part – 3D object

Extends Instance with:

- Size – Vector3
- Position – Vector3
- Orientation – Vector3
- Color – Color3
- Material – string (e.g., "Plastic", "Metal")
- Transparency – float 0..1
- Reflectance – float 0..1
- Anchored – bool
- CanCollide – bool
- Velocity – Vector3
- RotVelocity – Vector3

Model

Extends Instance with:

- GetPrimaryPart() – returns the primary Part
- SetPrimaryPart(part) – sets the primary part

Tool

Extends Model with:

- CanEquip – bool
- RequiresHandle – bool
- Grip – CFrame
- Equip(player), Unequip(), Activate() – methods

Player

Represents a player:

- UserId – int
- DisplayName – string
- AccountAge – int
- Character – Model or nil
- LoadCharacter() – mock

Other instances

- Folder
- Script, ModuleScript, LocalScript (with Source property)
- ValueBase subclasses: BoolValue, NumberValue, StringValue, ObjectValue, Color3Value, Vector3Value, CFrameValue, BrickColorValue, IntValue, DoubleValue

---

Services

All Roblox services are available as children of the global game object.

Players

- GetPlayers() – list of all Player objects
- GetPlayerByUserId(id) – returns player or nil
- GetPlayerByName(name) – returns player or nil
- CreatePlayer(user_id, name) – creates a new player (mock)

DataStoreService

- GetDataStore(name, scope=None) – returns a mock data store (a LuauTable)

HttpService

- HttpEnabled – bool (mock)
- GetAsync(url, headers=None) – returns "{}"
- PostAsync(url, data, content_type="application/json") – returns "{}"
- RequestAsync(options) – returns mock response dict
- JSONDecode(data) – uses Python json.loads
- JSONEncode(data) – uses Python json.dumps

RunService

- Heartbeat
-  _Event that fires every frame (mock)
- Stepped – event
- RenderStepped – event
- IsServer() – always True (mocks server)
- IsClient() – always False
- IsStudio() – always False

TweenService

- Create(instance, tween_info, properties) – returns a mock tween with play(), cancel(), etc.
- GetTweenInfo(duration, easing_style, easing_direction, repeat_count=0, reverses=False, delay_time=0) – returns info table

Lighting

- Brightness – float
- ClockTime – float (hour 0-24)
- Ambient – Color3

SoundService

- Volume – float
- DistanceFactor – float

UserInputService

- MouseEnabled – bool
- MouseBehaviour – string

ContextActionService

- BindAction(action_name, callback, create_button=True, touch_screen_controls=None) – dummy
- UnbindAction(action_name) – dummy

MarketplaceService

- CanPurchase(player, product_id) – returns True
- PurchaseProduct(player, product_id) – returns True

TeleportService

- Teleport(place_id, players, options=None) – dummy

GuiService

- GetGuiInset() – returns Rect(0,0,0,0)

TextService

- FilterAsync(text, from_user_id, context) – returns text (no filtering)

PathfindingService

- CreatePath(options=None) – returns table with ComputeAsync, GetWaypoints, IsBlocked (all mock)

CollectionService

- AddTag(instance, tag), RemoveTag(instance, tag), HasTag(instance, tag), GetTagged(tag), GetTags(instance), IsInstanceInTag(instance, tag) – tag management

Other services: ReplicatedStorage, ServerStorage, ServerScriptService, StarterGui, StarterPack, StarterPlayer.

---

Events

The library provides a simple event system:

```
event = luaxune._Event()  # internal, but also exposed via Instance properties
event.connect(lambda x: print("Got", x))
event.fire(42)            # prints "Got 42"
connection = event.connect(func)
connection()              # disconnects
```

Most instance properties like Changed, AncestryChanged, and service events (e.g., RunService.Heartbeat) are _Event objects.

---

Enums

luaxune.Enum is a container for enumeration items.

```
enum = luaxune.Enum("MyEnum", {"One": 1, "Two": 2})
print(enum.One)           # EnumItem("One", 1)
print(enum["Two"])        # EnumItem("Two", 2)
for item in enum:
    print(item.name, item.value)
```

A predefined Normal item is available.

---

Usage

Metatables on LuauTables

Luaxune implements _LuauTable which supports metatables for custom behavior:

```
t = luaxune._LuauTable()
mt = luaxune._LuauTable()
mt["__index"] = lambda self, key: "default"
luaxune.setmetatable(t, mt)
print(t["foo"])          # "default"
```

### Raw operations

Use rawget, rawset, rawlen to bypass metatables.


## Example Script :
```
import luaxune
import time

game = luaxune.game
player = game.Players.CreatePlayer(1, "Hero")

# Create a part and move it
part = luaxune.Part()
part.Name = "MovingPart"
part.Size = luaxune.Vector3(2, 2, 2)
part.Color = luaxune.Color3.from_rgb(0, 255, 0)
part.Parent = game.Workspace

# Animate via RunService (simulated)
def on_heartbeat(dt):
    part.Position += luaxune.Vector3(1, 0, 0) * dt
    print(f"Part at {part.Position}")

connection = game.RunService.Heartbeat.connect(on_heartbeat)

# Simulate 5 seconds of loop
start = time.time()
while time.time() - start < 5:
    game.RunService.Heartbeat.fire(0.016)   # mock 60 fps
    time.sleep(0.016)

connection()  # disconnect
part.Destroy()
```

Enjoy using Luaxune!
