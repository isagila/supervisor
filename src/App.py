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

class App:

  def __init__(self):
    self._folder = os.path.abspath("projects")
    self._storage = os.path.abspath("storage")
    self._last_update = os.path.abspath("last_updated.txt")
    self._period = 10

    self._projects = []
    for title, options in JSONFile("watched.json").read().items():
      self._projects.append(Project(
        os.path.join(self.)
      ))

    if os.path.exists(self._folder):
      Process.execute(f"rm -rf {self._folder}")
    os.mkdir(self._folder)
  
    with TextFile("w", self._last_update) as file:
      file.write(self._get_current_date())
    signal.signal(signal.SIGTERM, self._at_exit)
  
  def run(self):
    today = self._get_current_date()
    for project in self._projects:
      project.install()
      project.run(today)
    
    while True:
      today = self._get_current_date()
      need_new_logs = self._check_daily_log_update(today)

      for project in self._projects:
        if (
          project.have_updates() or
          not project.is_alive() or
          need_new_logs
        ):
          project.stop()
          project.update()
          project.run(today)

      time.sleep(self._period)
  
  def _check_daily_log_update(self, today):
    with TextFile("r", self._last_update) as file:
      last_update = file.read()
    
    if last_update != today:
      with TextFile("w", self._last_update) as file:
        file.write(today)
      return True
    return False
  
  @staticmethod
  def _get_current_date():
    return datetime.datetime.today.strftime("%d_%m_%Y")

  def _at_exit(self, *_):
    for project in self._projects:
      project.stop()
    sys.exit()

if __name__ == "__main__":
  App().run()
