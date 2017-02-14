import radb
import subprocess
import re


def execute(command):
    p = subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout.strip()


device = radb.promote_for_device()
result = execute(radb.build_cmd('shell dumpsys window windows', device))
# command = "adb shell dumpsys window windows"
# result = execute(command)
match = re.search('mCurrentFocus.*', result)
if match is not None:
    print match.group(0)
match = re.search('mFocusedApp.*', result)
if match is not None:
    print match.group(0)
input("Press Enter to continue")
