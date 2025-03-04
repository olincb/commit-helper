__all__ = ["diff", "diff_cached", "status"]
import subprocess
import rich

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
        rich.print("Running [bold magenta]git diff --chached[/]")
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
