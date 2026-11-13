from pathlib import Path
import json

import click as ck

from get_submodules import get_submodules
from positive_integer import PositiveInteger


@ck.command()
@ck.option("-p", "--path", type = ck.Path(exists = True, file_okay = False, readable = True, resolve_path = True, path_type = Path), default = ".", help = "The path of a Git repository to explore.")
def explore(path):
    submodules = get_submodules(path)
    s = json.dumps(submodules, default = lambda x: x.__dict__, indent = 4)
    print(s)

if __name__ == "__main__":
    explore()
