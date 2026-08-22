class _LuauTable:
    def __init__(self, dict_=None):
        self._dict = dict_ if dict_ is not None else {}
        self._metatable = None
    def __getitem__(self, key):
        if key in self._dict: return self._dict[key]
        if self._metatable and self._metatable.get("__index"):
            index = self._metatable["__index"]
            if callable(index): return index(self, key)
            return index.get(key)
        return nil
    def __setitem__(self, key, value):
        if self._metatable and self._metatable.get("__newindex"):
            newindex = self._metatable["__newindex"]
            if callable(newindex): newindex(self, key, value)
            else: newindex[key] = value
        else: self._dict[key] = value
    def __len__(self): return len(self._dict)
    def __iter__(self): return iter(self._dict)
    def __contains__(self, key): return key in self._dict
    def __call__(self, *args, **kwargs):
        if self._metatable and self._metatable.get("__call"):
            return self._metatable["__call"](self, *args, **kwargs)
        raise TypeError("table is not callable")
    def __add__(self, other):
        if self._metatable and self._metatable.get("__add"): return self._metatable["__add"](self, other)
        raise TypeError("attempt to add tables")
    def __sub__(self, other):
        if self._metatable and self._metatable.get("__sub"): return self._metatable["__sub"](self, other)
        raise TypeError("attempt to subtract tables")
    def __mul__(self, other):
        if self._metatable and self._metatable.get("__mul"): return self._metatable["__mul"](self, other)
        raise TypeError("attempt to multiply tables")
    def __div__(self, other):
        if self._metatable and self._metatable.get("__div"): return self._metatable["__div"](self, other)
        raise TypeError("attempt to divide tables")
    def __mod__(self, other):
        if self._metatable and self._metatable.get("__mod"): return self._metatable["__mod"](self, other)
        raise TypeError("attempt to modulo tables")
    def __pow__(self, other):
        if self._metatable and self._metatable.get("__pow"): return self._metatable["__pow"](self, other)
        raise TypeError("attempt to power tables")
    def __neg__(self):
        if self._metatable and self._metatable.get("__unm"): return self._metatable["__unm"](self)
        raise TypeError("attempt to unary minus")
    def __eq__(self, other):
        if self._metatable and self._metatable.get("__eq"): return self._metatable["__eq"](self, other)
        return self is other
    def __lt__(self, other):
        if self._metatable and self._metatable.get("__lt"): return self._metatable["__lt"](self, other)
        raise TypeError("attempt to compare tables")
    def __le__(self, other):
        if self._metatable and self._metatable.get("__le"): return self._metatable["__le"](self, other)
        raise TypeError("attempt to compare tables")
    def __str__(self):
        if self._metatable and self._metatable.get("__tostring"): return self._metatable["__tostring"](self)
        return "table: " + hex(id(self))
    def __repr__(self): return str(self)
    def _rawget(self, key): return self._dict.get(key, nil)
    def _rawset(self, key, value): self._dict[key] = value
    def _rawlen(self): return len(self._dict)
    def _get_metatable(self): return self._metatable
    def _set_metatable(self, mt): self._metatable = mt

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x); self.y = float(y); self.z = float(z)
    def __add__(self, o): return Vector3(self.x+o.x, self.y+o.y, self.z+o.z)
    def __sub__(self, o): return Vector3(self.x-o.x, self.y-o.y, self.z-o.z)
    def __mul__(self, s): return Vector3(self.x*s, self.y*s, self.z*s)
    def __rmul__(self, s): return self.__mul__(s)
    def __truediv__(self, s): return Vector3(self.x/s, self.y/s, self.z/s)
    def __neg__(self): return Vector3(-self.x, -self.y, -self.z)
    def __eq__(self, o): return self.x==o.x and self.y==o.y and self.z==o.z
    def __repr__(self): return f"Vector3({self.x}, {self.y}, {self.z})"
    def magnitude(self): return (self.x**2+self.y**2+self.z**2)**0.5
    def unit(self): return self / self.magnitude() if self.magnitude()>0 else Vector3(0,0,0)
    def dot(self, o): return self.x*o.x + self.y*o.y + self.z*o.z
    def cross(self, o): return Vector3(self.y*o.z-self.z*o.y, self.z*o.x-self.x*o.z, self.x*o.y-self.y*o.x)
    def lerp(self, o, t): return self + (o-self)*t

class CFrame:
    def __init__(self, x=0, y=0, z=0, qx=0, qy=0, qz=0, qw=1):
        self.position = Vector3(x,y,z)
        self.qx = qx; self.qy = qy; self.qz = qz; self.qw = qw
    @staticmethod
    def new(x=0, y=0, z=0): return CFrame(x,y,z)
    @staticmethod
    def look_at(pos, target, up=Vector3(0,1,0)): return CFrame(pos.x,pos.y,pos.z)
    def to_matrix(self): return [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    def __mul__(self, o):
        if isinstance(o, Vector3): return Vector3(o.x,o.y,o.z)
        return CFrame(self.position.x,self.position.y,self.position.z)
    def __repr__(self): return f"CFrame({self.position.x},{self.position.y},{self.position.z})"

class Color3:
    def __init__(self, r=0, g=0, b=0): self.r=r; self.g=g; self.b=b
    @staticmethod
    def from_rgb(r,g,b): return Color3(r/255,g/255,b/255)
    @staticmethod
    def from_hsv(h,s,v): return Color3(h,s,v)
    def __repr__(self): return f"Color3({self.r},{self.g},{self.b})"

class Rect:
    def __init__(self, x0=0, y0=0, x1=0, y1=0): self.x0=x0; self.y0=y0; self.x1=x1; self.y1=y1

class UDim:
    def __init__(self, scale=0, offset=0): self.scale=scale; self.offset=offset

class UDim2:
    def __init__(self, xs=0, xo=0, ys=0, yo=0): self.x=UDim(xs,xo); self.y=UDim(ys,yo)

nil = None
