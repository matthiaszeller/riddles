import subprocess
import shlex
from pathlib import Path


def exec_cmd(cmd: str, text: bool = True):
    cmd = shlex.split(cmd)
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        check=True
    ).stdout.strip()


def git_current_branch():
    return exec_cmd('git rev-parse --abbrev-ref HEAD')


def git_show_commit(name_only: bool = True):
    return exec_cmd(f'git show {"--name-only" if name_only else ""}')


def git_commit_riddle(year: str, day: str, part2: bool = True, base_path: Path = Path('src')):
    if git_current_branch() in {'main', 'master'}:
        raise ValueError('Cannot commit to main/master branch')

    if not part2:
        file_part2 = base_path.joinpath(year, day, 'part2.py')
        assert file_part2.exists(), f'failed to exclude part 2: {file_part2} does not exist'

    # Add folder
    exec_cmd(f'git add {base_path.joinpath(year, day)}')

    if not part2:
        exec_cmd(f'git restore --staged {file_part2}')

    # Commit
    exec_cmd(f'git commit -m "{year}-{day} part 1{" & 2" if part2 else ""}"')

    # Show
    print(git_show_commit())


if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('year', type=str)
    p.add_argument('day', type=str)
    p.add_argument('--partial', action='store_true')
    args = p.parse_args()

    git_commit_riddle(args.year, args.day, not args.partial)
