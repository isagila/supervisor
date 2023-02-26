import os

from Process import Process
from files import (
  JSONFile,
  TextFile,
)

class Project:

  def __init__(self, folder, storage, title, options):
    self._folder = os.path.join(folder, title)
    self._storage = os.path.join(storage, title)
    self._title = title
    self._url = f"https://github.com/{options['repo']}.git"
    self._branch = options["branch"]
    self._command = options["command"]

    self._process = None
  
  def install(self):
    if not os.path.exists(self._storage):
      os.mkdir(self._storage)

    settings_path = os.path.join(self._storage, "project.json")
    settings_str = "{}"
    if os.path.exists(settings_path):
      with TextFile("r", settings_path) as file:
        settings_str = file.read()
    settings_str = settings_str.replace("$PATH$", self._storage)
    with TextFile("w", settings_path) as file:
      file.write(settings_str)

    root_folder = os.path.normpath(os.path.join(self._folder, ".."))
    if os.path.exists(os.path.join(self._folder)):
      Process.execute(
        f"rm -rf {self._title}",
        cwd = root_folder
      )
    Process.execute(
      f"git clone {self._url} {self._title}",
      cwd = root_folder
    )

  def run(self):
    settings_path = os.path.join(self._storage, "project.json")
    self._process = Process(
      f"{self._command} {settings_path}",
      cwd = self._folder
    )
  
  def have_updates(self):
    Process.execute("git fetch", cwd = self._folder)
    diff = Process.execute(
      f"git diff origin/{self._branch} {self._branch} --name-only",
      cwd = self._folder
    )
    return diff != ""
  
  def update(self):
    if not self.is_alive():
      Process.execute("git pull", cwd = self._folder)

  def stop(self):
    self._process.terminate()
    self._process = None
  
  def is_alive(self):
    if self._process is None:
      return False
    return self._process.is_alive()
  