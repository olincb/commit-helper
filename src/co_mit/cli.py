import asyncio
import os

import rich
import rich_click as click

from . import commit


@click.command()
@click.option(
    "--openai-key",
    "-k",
    type=click.STRING,
    help="OpenAI API key. Can also set with OPENAI_API_KEY environment variable.",
)
def main(openai_key: str | None):
    """Helps with git commits."""

    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    rich.print("Generating commit message...")
    asyncio.run(commit.co_mit())
