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

    self._log = None
    self._process = None
  
  def _touch_folder(self, *parts): # create if not exists
    path = os.path.join(*parts)
    if not os.path.exists(path):
      os.mkdir(path)

  def install(self):
    self._touch_folder(self._storage)
    self._touch_folder(self._storage, "logs")

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

  def run(self, today):
    self._log = TextFile(os.path.join(
      self._storage, "logs", f"log_{today}.txt"
    ))
    settings_path = os.path.join(self._storage, "project.json")
    self._process = Process(
      f"{self._command} {settings_path}",
      output = self._log.body()
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
    self._log.close()

    self._process = self._log = None
  
  def is_alive(self):
    if self._process is None:
      return False
    return self._process._is_alive()
  