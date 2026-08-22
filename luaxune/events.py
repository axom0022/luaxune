class _Event:
    def __init__(self):
        self._callbacks = []
    def connect(self, callback):
        self._callbacks.append(callback)
        return lambda: self._callbacks.remove(callback)
    def fire(self, *args):
        for cb in self._callbacks:
            cb(*args)
