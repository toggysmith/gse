from pathlib import Path
import json

import click as ck

from get_submodules import get_submodules
from positive_integer import PositiveInteger


@ck.command()
@ck.option("-p", "--path", type = ck.Path(exists = True, file_okay = False, readable = True, resolve_path = True, path_type = Path), default = ".", help = "The path of a Git repository to explore.")
def explore(path):
    submodules = get_submodules(path)
    with open("graph.json", "w") as f:
        json.dump(submodules, f, default = lambda x: x.__dict__, ensure_ascii = False, indent = 4)

if __name__ == "__main__":
    explore()
