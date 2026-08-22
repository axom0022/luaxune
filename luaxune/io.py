import os as _os
import shutil as _shutil

class _fileobj:
    def __init__(self, path, mode):
        self._handle = open(path, mode)
    def read(self, n=-1):
        return self._handle.read(n)
    def write(self, data):
        self._handle.write(data)
    def close(self):
        self._handle.close()

def _io_open(path, mode='r'):
    return _fileobj(path, mode)

def _io_read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def _io_write(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)

def _io_append(path, data):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(data)

def _io_listdir(path):
    return _os.listdir(path)

def _io_mkdir(path):
    _os.makedirs(path, exist_ok=True)

def _io_remove(path):
    if _os.path.isdir(path):
        _shutil.rmtree(path)
    else:
        _os.remove(path)

def _io_rename(old, new):
    _os.rename(old, new)

def _io_exists(path):
    return _os.path.exists(path)

def _io_isfile(path):
    return _os.path.isfile(path)

def _io_isdir(path):
    return _os.path.isdir(path)

_iotable = {
    'open': _io_open,
    'read': _io_read,
    'write': _io_write,
    'append': _io_append,
    'listdir': _io_listdir,
    'mkdir': _io_mkdir,
    'remove': _io_remove,
    'rename': _io_rename,
    'exists': _io_exists,
    'isfile': _io_isfile,
    'isdir': _io_isdir,
      }
