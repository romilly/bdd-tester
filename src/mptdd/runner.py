from time import sleep

import subprocess
import sys

sys.path += '/home/romilly/git/active/bdd-tester/src'

processes = []
for script in ['src/mptdd/controller.py','tests/e2e/button_print.py','tests/e2e/button_print.py']:
    print(script)
    processes.append(subprocess.Popen(['python']+[script],
                                      cwd='/home/romilly/git/active/bdd-tester',
                                  stdout=subprocess.PIPE))
sleep(1)
print(len(processes))
for process in processes:
    print(process.pid)
    process.wait()
    print(process.communicate())