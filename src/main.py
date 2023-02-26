import os
import sys
import signal

from Process import Process
from files import TextFile

def main():
  pid_file = "pid.txt"
  if len(sys.argv) == 1:
    if os.path.exists(pid_file):
      print("Server is running")
    else:
      print("Server isn't running")
  
  elif sys.argv[1] == "start":
    if os.path.exists(pid_file):
      print("Server is already running")
      return
    with TextFile("w", pid_file) as file:
      file.write(Process("python3 src/App.py").get_id())
    print("Server has been started")
  
  elif sys.argv[1] == "stop":
    if not os.path.exists(pid_file):
      print("Server isn't running yet")
      return
    try:
      with TextFile("r", pid_file) as file:
        pid = int(file.read())
      os.kill(pid, signal.SIGTERM)
      os.remove(pid_file)
      print("Server has been stopped")
    except Exception as exc:
      print("While server stopping following exception ocurred:")
      print(exc)
  
  else:
    print("Unknown command")
    print(f"Usage: {sys.argv[0]} [start|stop]")
  
if __name__ == "__main__":
  main()
