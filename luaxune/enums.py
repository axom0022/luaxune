class EnumItem:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __int__(self):
        return self.value
    def __eq__(self, other):
        if isinstance(other, EnumItem):
            return self.value == other.value
        return self.value == other

class Enum:
    def __init__(self, name, items):
        self.name = name
        self._items = {}
        for k, v in items.items():
            item = EnumItem(k, v)
            setattr(self, k, item)
            self._items[v] = item
    def __iter__(self):
        return iter(self._items.values())
    def __getitem__(self, key):
        return self._items.get(key)

Normal = EnumItem('Normal', 0)
Enum = Enum('Enum', {'Normal': 0})
