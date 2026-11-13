import click as ck
import sys
from pathlib import Path

class PositiveInteger(ck.ParamType[int]):
    name = "integer"

    def convert(self, value, param, ctx) -> int:
        try:
            value = int(value)

            if value < 1:
                self.fail(f"{value!r} is not a positive integer", param, ctx)

            return value
        except ValueError:
            self.fail(f"{value!r} is not a valid integer", param, ctx)

@ck.command()
@ck.option("-d", "--maxdepth", type = PositiveInteger(), help = "The maximum depth to explore down.")
@ck.option("-p", "--path", type = ck.Path(exists = True, file_okay = False, readable = True, resolve_path = True, path_type = Path), default = ".", help = "The path of a Git repository to explore.")
def explore(maxdepth, path):
    ck.echo(f"The max depth is {maxdepth} and the path is {path}.")

if __name__ == "__main__":
    explore()
