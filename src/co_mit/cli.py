import rich_click as click

from . import commit

@click.command()
def main():
    """Helps with git commits."""
    commit.co_mit()
