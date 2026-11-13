import click as ck
import sys
from pathlib import Path

@ck.command()
@ck.option("-d", "--maxdepth", type = ck.IntRange(1, sys.maxsize), help = "The maximum depth to explore down.")
@ck.option("-p", "--path", type = ck.Path(exists = True, file_okay = False, readable = True, resolve_path = True, path_type = Path), default = ".", help = "The path of a Git repository to explore.")
def explore(maxdepth, path):
    ck.echo(f"The max depth is {maxdepth} and the path is {path}.")

if __name__ == "__main__":
    explore()
