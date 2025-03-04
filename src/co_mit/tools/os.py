__all__ = ["read_file"]
import rich


from .. import config


def read_file(file_path: str) -> str:
    """Read the contents of a file and return it as a string.

    Helpful when additional context is required for a particular file,
    outside of what is included in the `git diff`.

    """
    if not config.Config.quiet:
        rich.print(f"Reading file at [bold magenta]{file_path}[/]")
    with open(file_path, "r") as file:
        return file.read()
