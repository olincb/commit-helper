import asyncio
import os

import rich
import rich_click as click

from . import commit, config


@click.command()
@click.option(
    "--openai-key",
    "-k",
    type=click.STRING,
    help="OpenAI API key. Can also set with OPENAI_API_KEY environment variable.",
)
@click.option(
    "--example",
    "-e",
    type=click.STRING,
    help="Example input to generate a commit message from.",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress all output other than final commit message. Useful for scripting. Can also set with CO_MIT_QUIET environment variable.",
)
@click.option(
    "--version",
    "-v",
    is_flag=True,
    help="Show version information.",
)
def main(openai_key: str | None, example: str | None, quiet: bool, version: bool) -> None:
    """Helps with git commits."""

    if version:
        from . import __about__

        click.echo(f"co-mit version {__about__.__version__}")
        return

    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    if quiet:
        config.Config.quiet = quiet
    else:
        rich.print("Generating commit message...")
    asyncio.run(commit.co_mit(example))
