import os
import json

class File:

  def __init__(self, mode, *path):
    self._body = open(os.path.join(*path), mode, encoding="utf8")
  
  def __enter__(self):
    return self
  
  def __exit__(self, exception_type, exception_value, traceback):
    self._body.close()
  
  def close(self):
    self._body.close()
  
  def body(self):
    return self._body

class TextFile(File):
  
  def read(self):
    return self._body.read()
  
  def readlines(self):
    yield self._body.readline()

  def write(self, value):
    self._body.write(str(value))

class JSONFile(File):
  
  def read(self):
    return json.loads(self._body.read())

  def write(self, data):
    self._body.write(json.dumps(data))
