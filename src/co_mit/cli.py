import rich
import rich_click as click


@click.command()
@click.option(
    "--openai-api-key",
    "-k",
    type=click.STRING,
    help="OpenAI API key. Can also set with CO_MIT_OPENAI_API_KEY environment variable.",
)
@click.option(
    "--example",
    "-e",
    type=click.STRING,
    help="Example input to generate a commit message from. Can also set with CO_MIT_EXAMPLE environment variable.",
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
    openai_api_key: str | None, example: str | None, quiet: bool, version: bool
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
        rich.print("[bold yellow]Generating commit message...[/]")

    # Lazy imports to speed up --help and --version
    import asyncio
    from . import commit

    if example:
        config.Config.example = example
    if openai_api_key:
        config.Config.openai_api_key = openai_api_key
    asyncio.run(commit.co_mit(example))
