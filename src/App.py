import os
import sys
import time
import shutil
import signal
import datetime

from Process import Process
from files import (
  JSONFile,
  TextFile,
)
from Project import Project

class App:

  def __init__(self):
    self._folder = os.path.abspath("projects")
    self._storage = os.path.abspath("storage")
    self._period = 10

    self._projects = []
    for title, options in JSONFile("r", "watched.json").read().items():
      self._projects.append(Project(
        self._folder,
        self._storage,
        title,
        options
      ))

    if os.path.exists(self._folder):
      Process.execute(f"rm -rf {self._folder}")
    os.mkdir(self._folder)
    if not os.path.exists(self._storage):
      os.mkdir(self._storage)

    signal.signal(signal.SIGTERM, self._at_exit)
  
  def run(self):
    for project in self._projects:
      project.install()
      project.run()
    
    while True:
      for project in self._projects:
        if project.have_updates() or not project.is_alive():
          project.stop()
          project.update()
          project.run(today)

      time.sleep(self._period)

  def _at_exit(self, *_):
    for project in self._projects:
      project.stop()
    sys.exit()

if __name__ == "__main__":
  App().run()
