__all__ = ['diff']
import subprocess

def diff():
    return subprocess.check_output(['git', 'diff'], text=True)

def status():
    return subprocess.check_output(['git', 'status'], text=True)
