from .types import Vector3, CFrame, Color3, nil
from .events import _Event

class Instance:
    def __init__(self, class_name="Instance"):
        self._class_name = class_name
        self._name = class_name
        self._parent = nil
        self._children = {}
        self._properties = {}
        self._tags = set()
        self._changed = _Event()
        self._child_added = _Event()
        self._child_removed = _Event()
        self._descendant_added = _Event()
        self._descendant_removed = _Event()
        self._ancestry_changed = _Event()
        self._archivable = True
        self._locked = False
        self._property_changed = _Event()
    @property
    def Name(self): return self._name
    @Name.setter
    def Name(self, value):
        old = self._name; self._name = value
        self._changed.fire("Name", old, value)
    @property
    def ClassName(self): return self._class_name
    @property
    def Parent(self): return self._parent
    @Parent.setter
    def Parent(self, value):
        if self._parent: self._parent._children.pop(self._name, nil)
        self._parent = value
        if value: value._children[self._name] = self
        self._ancestry_changed.fire(self, value)
    def GetFullName(self):
        if self._parent: return self._parent.GetFullName() + "." + self._name
        return self._name
    def FindFirstChild(self, name, recursive=False):
        if name in self._children: return self._children[name]
        if recursive:
            for child in self._children.values():
                res = child.FindFirstChild(name, True)
                if res: return res
        return nil
    def WaitForChild(self, name, timeout=None):
        import time
        start = time.time()
        while True:
            child = self.FindFirstChild(name)
            if child: return child
            if timeout and time.time() - start > timeout: return nil
            time.sleep(0.01)
    def GetChildren(self): return list(self._children.values())
    def GetDescendants(self):
        result = []
        for child in self._children.values():
            result.append(child)
            result.extend(child.GetDescendants())
        return result
    def IsA(self, class_name): return self._class_name == class_name
    def Clone(self, parent=nil):
        new = Instance(self._class_name)
        new._name = self._name
        new._properties = self._properties.copy()
        new._tags = self._tags.copy()
        if parent: new.Parent = parent
        return new
    def Destroy(self):
        self.Parent = nil
        self._children.clear()
    def AddTag(self, tag): self._tags.add(tag)
    def HasTag(self, tag): return tag in self._tags
    def RemoveTag(self, tag): self._tags.discard(tag)
    def GetTags(self): return list(self._tags)
    def GetAttribute(self, attr): return self._properties.get(attr, nil)
    def SetAttribute(self, attr, value):
        self._properties[attr] = value
        self._property_changed.fire(attr, value)
    def GetAttributes(self): return self._properties.copy()
    def ClearAttributes(self): self._properties.clear()
    def GetDebugId(self): return hex(id(self))
    def GetDebugChildren(self): return self.GetChildren()
    def GetDebugString(self): return f"{self._class_name}: {self._name}"
    def __repr__(self): return f"Instance({self._class_name}, {self._name})"

class Folder(Instance):
    def __init__(self): super().__init__("Folder")

class Part(Instance):
    def __init__(self):
        super().__init__("Part")
        self._size = Vector3(1,1,1)
        self._position = Vector3(0,0,0)
        self._orientation = Vector3(0,0,0)
        self._color = Color3(1,1,1)
        self._material = "Plastic"
        self._transparency = 0
        self._reflectance = 0
        self._anchored = False
        self._can_collide = True
        self._locked = False
        self._velocity = Vector3(0,0,0)
        self._rot_velocity = Vector3(0,0,0)
    @property
    def Size(self): return self._size
    @Size.setter
    def Size(self, v): self._size = v
    @property
    def Position(self): return self._position
    @Position.setter
    def Position(self, v): self._position = v
    @property
    def Orientation(self): return self._orientation
    @Orientation.setter
    def Orientation(self, v): self._orientation = v
    @property
    def Color(self): return self._color
    @Color.setter
    def Color(self, c): self._color = c
    @property
    def Material(self): return self._material
    @Material.setter
    def Material(self, m): self._material = m
    @property
    def Transparency(self): return self._transparency
    @Transparency.setter
    def Transparency(self, t): self._transparency = t
    @property
    def Reflectance(self): return self._reflectance
    @Reflectance.setter
    def Reflectance(self, r): self._reflectance = r
    @property
    def Anchored(self): return self._anchored
    @Anchored.setter
    def Anchored(self, a): self._anchored = a
    @property
    def CanCollide(self): return self._can_collide
    @CanCollide.setter
    def CanCollide(self, c): self._can_collide = c
    @property
    def Velocity(self): return self._velocity
    @Velocity.setter
    def Velocity(self, v): self._velocity = v
    @property
    def RotVelocity(self): return self._rot_velocity
    @RotVelocity.setter
    def RotVelocity(self, v): self._rot_velocity = v

class Model(Instance):
    def __init__(self): super().__init__("Model")
    def GetPrimaryPart(self): return self.FindFirstChild("PrimaryPart")
    def SetPrimaryPart(self, part):
        part.Name = "PrimaryPart"
        part.Parent = self

class Tool(Instance):
    def __init__(self):
        super().__init__("Tool")
        self._can_equip = True
        self._requires_handle = True
        self._grip = CFrame.new(0,0,0)
    @property
    def CanEquip(self): return self._can_equip
    @CanEquip.setter
    def CanEquip(self, b): self._can_equip = b
    @property
    def RequiresHandle(self): return self._requires_handle
    @RequiresHandle.setter
    def RequiresHandle(self, b): self._requires_handle = b
    @property
    def Grip(self): return self._grip
    @Grip.setter
    def Grip(self, c): self._grip = c
    def Equip(self, player): pass
    def Unequip(self): pass
    def Activate(self): pass

class Player(Instance):
    def __init__(self):
        super().__init__("Player")
        self._user_id = 0
        self._display_name = "Player"
        self._account_age = 0
        self._character = nil
    @property
    def UserId(self): return self._user_id
    @UserId.setter
    def UserId(self, id): self._user_id = id
    @property
    def DisplayName(self): return self._display_name
    @DisplayName.setter
    def DisplayName(self, name): self._display_name = name
    @property
    def AccountAge(self): return self._account_age
    @AccountAge.setter
    def AccountAge(self, age): self._account_age = age
    @property
    def Character(self): return self._character
    @Character.setter
    def Character(self, char): self._character = char
    def LoadCharacter(self): pass
