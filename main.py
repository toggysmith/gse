from pathlib import Path
import json
import enum
import hashlib

import click as ck

from get_submodules import get_submodules, get_repo_name_from_url
from positive_integer import PositiveInteger
from git import git


class Format(enum.Enum):
    DOT = enum.auto()

@ck.group()
def cli():
    pass

@cli.command()
@ck.option("-p", "--path", type = ck.Path(exists = True, file_okay = False, readable = True, resolve_path = True, path_type = Path), default = ".", help = "The path of a Git repository to explore.")
def explore(path):
    current_repo_url = git(path, ["remote", "get-url", "origin"]).decode().strip()
    current_repo = get_repo_name_from_url(current_repo_url)

    submodules = get_submodules(path)
    head = {
        "project": current_repo[0],
        "repo": current_repo[1],
        "absolute_path": str(path),
        "relative_path": "/",
        "url": current_repo_url,
        "children": submodules
    }
    with open("graph.json", "w") as f:
        json.dump([head], f, default = lambda x: x.__dict__, ensure_ascii = False, indent = 4)

@cli.command()
@ck.option("-s", "--src", type = ck.Path(exists = True, dir_okay = False, readable = True, resolve_path = True, path_type = Path), default = "graph.json", help = "The path of the graph JSON to transform.")
@ck.option("-f", "--fmt", type = ck.Choice(Format, case_sensitive = False), default = Format.DOT, help = "The format to transform the graph JSON into.")
@ck.option("-d", "--dst", type = ck.Path(exists = False, dir_okay = False, resolve_path = True, path_type = Path), default = "graph.dot", help = "The path to the file to output the transformed graph JSON into.")
def transform(src, fmt, dst):
    with open("graph.json", "r") as f:
        graph = json.load(f)

    def write_to_f(f, node, parent = None):
        name = f"{node['project']}/{node['repo']}"
        f.write(f'"{name}"\n')

        if 'children' in node:
            for child in node['children']:
                child_name = f"{child['project']}/{child['repo']}"
                f.write(f'"{name}" -> "{child_name}"\n')
                write_to_f(f, child, parent = node)

    with open("graph.dot", "w") as f:
        f.write("digraph G {\n")
        for node in graph:
            print(node)
            write_to_f(f, node)
        f.write("}\n")

if __name__ == "__main__":
    cli()
