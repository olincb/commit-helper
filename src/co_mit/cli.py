import rich
import rich_click as click

from . import config


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
@click.option(
    "--show-config",
    "-c",
    is_flag=True,
    help="Show current configuration.",
)
def main(
    openai_api_key: str | None,
    example: str | None,
    quiet: bool,
    version: bool,
    show_config: bool,
) -> None:
    """Helps with git commits."""

    # Set configuration options
    if openai_api_key:
        config.Config.openai_api_key = openai_api_key
    if example:
        config.Config.example = example
    if quiet:
        config.Config.quiet = quiet

    # Handle alternative commands
    if version:
        from . import __about__

        click.echo(f"co-mit version {__about__.__version__}")
        return
    if show_config:
        import json

        cfg = config.Config.model_dump()
        if cfg["openai_api_key"]:
            cfg["openai_api_key"] = cfg["openai_api_key"][:4] + "*" * 16
        rich.print(json.dumps(cfg, indent=4))
        return

    # Echo before lazy importing to speed up initial message
    if not config.Config.quiet:
        rich.print("[bold yellow]Generating commit message...[/]")

    # Lazy imports to speed up commands that won't run this code
    import asyncio
    from . import commit

    asyncio.run(commit.co_mit())
