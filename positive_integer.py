import click as ck

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

