from pathlib import Path


Command = tuple[str, list[str]]


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str) -> list[Command]:
    lines = data.splitlines()
    assert lines[0] == '$ cd /'
    commands = []
    cmd, buffer = 'cd /', []

    for line in lines[1:]:
        if line.startswith('$'):
            commands.append((cmd, buffer))
            buffer = []

            cmd = line.strip('$ ')

        else:
            buffer.append(line)

    commands.append((cmd, buffer))
    return commands




class File:

    def __init__(self, name: str, is_dir: bool = False, size: int = None, parent: 'File' = None):
        self.name = name
        self.is_dir = is_dir
        self.size = size
        self.parent = parent
        self.children: dict[str, 'File'] = {}
        self._total_size = None

        if self.parent is not None:
            self.parent.children[self.name] = self

            if self.is_dir:
                self.children['..'] = self.parent

    @property
    def total_size(self) -> int:
        if not self.is_dir:
            return self.size

        if self._total_size is None:
            self._total_size = sum(child.total_size for n, child in self.children.items() if n != '..')

        return self._total_size

    def __repr__(self):
        desc = 'dir' if self.is_dir else f'file, size={self.size}'
        return f'{self.name} ({desc})'

    def tree(self):
        lines = []
        q = [(0, self)]
        while len(q) > 0:
            depth, file = q.pop()
            indent = ' ' * 2 * depth
            lines.append(f'{indent}- {file}')

            if file.is_dir:
                q.extend((depth+1, f) for n, f in file.children.items() if n != '..')

        return '\n'.join(lines)

    def walk(self, only_dirs: bool = False):
        q = [self]
        while len(q) > 0:
            file = q.pop()
            q.extend(f for n, f in file.children.items() if n != '..')

            if not file.is_dir and only_dirs:
                continue

            yield file


def build_tree(data: list[Command]):
    root = File(name='/', is_dir=True)
    cwd = root
    for cmd, out in data[1:]:
        if cmd.startswith('ls'):
            for item in out[::-1]:
                desc, name = item.split(' ', 1)
                if desc == 'dir':
                    is_dir = True
                    size = None
                else:
                    is_dir = False
                    size = int(desc)

                child = File(name=name, is_dir=is_dir, size=size, parent=cwd)

        else:
            cd_into = cmd.split()[1]
            cwd = cwd.children[cd_into]

    return root


example = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
