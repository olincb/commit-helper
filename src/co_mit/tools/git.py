__all__ = ["diff", "diff_cached", "status"]
import subprocess
import rich
import rich_click as click

from .. import config


def diff() -> str:
    """Return the `git diff` as a string.

    Helpful for seeing all changes not staged for commit.

    """
    if not config.Config.quiet:
        rich.print("Running [bold magenta]git diff[/]")
    return subprocess.check_output(["git", "diff"], text=True)


def diff_cached() -> str:
    """Return the `git diff --cached` as a string.

    Helpful for seeing all changes already staged to be committed.

    """
    if not config.Config.quiet:
        rich.print("Running [bold magenta]git diff --cached[/]")
    return subprocess.check_output(["git", "diff", "--cached"], text=True)


def status() -> str:
    """Return the git status as a string.

    Helpful for seeing a summary of staged and unstaged changes.
    This is usually a good place to start when writing a commit message.

    """
    if not config.Config.quiet:
        rich.print("Running [bold magenta]git status[/]")
    return subprocess.check_output(["git", "status"], text=True)


def log(n: int = 5) -> str:
    """Return the git log as a string. Shows the last `n` commits (up to a maxiumum of 15).

    Helpful for seeing a summary of the commit history, and determining the
    timing of recent commits.

    """
    n = min(n, 15)
    if not config.Config.quiet:
        rich.print(f"Running [bold magenta]git log -n {n}[/]")
    return subprocess.check_output(["git", "log", "-n", str(n)], text=True)


def add(files: list[str]) -> str | None:
    """Add files to the git staging area.

    Use this to stage files for commit.

    Args:
        files (list[str]): A list of file paths to add.

    Returns:
        str | None: None if the operation was accepted and completed,
                    otherwise the feedback from the user about why the
                    operation was not accepted.

    """
    color_interleaved = [
        f"[bold light_sky_blue1]{file}[/]"
        if i % 2 == 0
        else f"[bold gold1]{file}[/]"
        for i, file in enumerate(files)
    ]
    rich.print(f"Request to run [bold magenta]git add [/]{' '.join(color_interleaved)}")
    rich.print("[bold yellow]Accept git add operation?[/]", end=" ")
    feedback = click.prompt('["Y/y/yes" or provide feedback]', type=str)
    if feedback.strip().lower() not in ["y", "yes"]:
        return feedback
    subprocess.run(["git", "add", *files])


def commit(message: str) -> str | None:
    """Commit the staged changes with the provided message.

    Args:
        message (str): The commit message.

    Returns:
        str | None: None if the operation was accepted and completed,
                    otherwise the feedback from the user about why the
                    operation was not accepted.

    """
    rich.print(
        f"Request to run [bold magenta]git commit -m [/][bold dark_orange3]'{message}'[/]"
    )

    # Display summary of changes using git status
    rich.print("Output of [bold magenta]git status -s[/]:")
    current_status = subprocess.check_output(
        ["git", "-c", "color.ui=always", "status", "-s"], text=True
    )
    print(current_status.strip())

    rich.print("[bold yellow]Accept commit operation?[/]", end=" ")
    feedback = click.prompt('["Y/y/yes" or provide feedback]', type=str)
    if feedback.strip().lower() not in ["y", "yes"]:
        return feedback
    subprocess.run(["git", "commit", "-m", f"'{message}'"])
