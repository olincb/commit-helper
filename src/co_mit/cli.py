import rich_click as click


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
def main(
    openai_key: str | None, example: str | None, quiet: bool, version: bool
) -> None:
    """Helps with git commits."""

    if version:
        from . import __about__

        click.echo(f"co-mit version {__about__.__version__}")
        return

    # Echo before lazy importing to speed up initial message
    from . import config
    if quiet:
        config.Config.quiet = quiet
    else:
        click.echo("Generating commit message...")

    # Lazy imports to speed up --help and --version
    import asyncio
    import os
    from . import commit

    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    asyncio.run(commit.co_mit(example))
