__all__ = ["diff", "diff_cached", "status"]
import subprocess
import rich


def diff() -> str:
    """Return the `git diff` as a string.

    Helpful for seeing all unstaged changes.

    """
    rich.print("running `git diff`")
    return subprocess.check_output(["git", "diff"], text=True)


def diff_cached() -> str:
    """Return the `git diff --cached` as a string.

    Helpful for seeing all staged changes.

    """
    rich.print("running `git diff --chached`")
    return subprocess.check_output(["git", "diff", "--cached"], text=True)


def status() -> str:
    """Return the git status as a string.

    Helpful for seeing a summary of staged and unstaged changes.

    """
    rich.print("running `git status`")
    return subprocess.check_output(["git", "status"], text=True)
