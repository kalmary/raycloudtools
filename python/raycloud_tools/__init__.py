from .trees import run_trees

__all__ = ["run_trees"]


def main():
    import os
    import sys

    from .trees import executable_path

    executable = os.fspath(executable_path())
    os.execv(executable, [executable, *sys.argv[1:]])
