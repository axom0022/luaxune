import time as _time

class _profiler:
    def __init__(self):
        self.records = {}
        self.current = None

    def start(self, name):
        self.current = name
        self.records[name] = {'start': _time.time(), 'calls': 0}

    def stop(self):
        if self.current:
            self.records[self.current]['end'] = _time.time()
            self.records[self.current]['duration'] = self.records[self.current]['end'] - self.records[self.current]['start']
            self.current = None

    def dump(self):
        return self.records

_prof = _profiler()

_profiletable = {
    'start': _prof.start,
    'stop': _prof.stop,
    'dump': _prof.dump,
}
