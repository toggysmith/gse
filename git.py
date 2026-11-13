import subprocess
import sys
from pathlib import Path


def git(cwd: Path, cmd: list[str]) -> str:
    if not isinstance(cmd, list):
        raise TypeError("Not a list!")
    if not all(isinstance(c, str) for c in cmd):
        raise TypeError("List is not all strings!")
    try:
        cmd = ["git", *cmd]
        output = subprocess.check_output(cmd,
                                         stderr = subprocess.STDOUT,
                                         cwd = cwd)
        return output
    except subprocess.CalledProcessError as e:
        print("ERROR: Running Git command resulted in the error:\n")
        print(e.output.decode()) 

        sys.exit(-1)
