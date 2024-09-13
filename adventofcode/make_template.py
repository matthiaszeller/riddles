"""
Example: to run by specifying the AOC_SESSION env variable:

"""
import argparse
import ast
import os
import shutil
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

import logging


logging.basicConfig(level=logging.INFO)

EXAMPLES_SEPARATOR = '\n\n§$@%\n\n'


URL = 'https://adventofcode.com/{year}/day/{day}'


def load_url(url: str, parse: bool = False, **kwargs) -> str | BeautifulSoup:
    response = requests.get(url, **kwargs)
    response.raise_for_status()

    text = response.text
    if parse:
        return BeautifulSoup(text, 'html.parser')

    return text


def get_aoc_url(year: int, day: int, join: str = '') -> str:
    if join:
        join = '/' + join.lstrip('/')
    return URL.format(year=year, day=day) + join


def aoc_session_cookie(session_value: str = None) -> dict:
    if session_value is None:
        session_value = os.getenv('AOC_SESSION')
        if session_value is None:
            print(os.environ)
            raise ValueError('AOC_SESSION env variable not set')

    if session_value.startswith('session='):
        session_value = session_value[8:]

    return {'session': session_value}


def get_aoc_input(year: int, day: int):
    return load_url(get_aoc_url(year, day, 'input'), cookies=aoc_session_cookie())


def get_aoc_code_blocks(year: int, day: int) -> list[str]:
    soup = load_url(get_aoc_url(year, day), parse=True, cookies=aoc_session_cookie())
    code_blocks = soup.find_all('code')
    # remove inline code blocks
    code_blocks = [
        txt
        for block in code_blocks
        if (txt := block.text.strip()).count('\n') > 1
    ]
    return code_blocks


def empty_folder(folder: Path):
    try:
        shutil.rmtree(folder)
    except FileNotFoundError:
        pass

    folder.mkdir()


def _extract_public_names(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parse the AST to find top-level definitions and assignments
    tree = ast.parse(''.join(lines), filename=file_path)

    public_names = {}
    current_block = None

    # Detect blocks based on lines starting with '# ---'
    for i, line in enumerate(lines):
        if line.strip().startswith('# ---'):
            # Start a new block for grouping
            current_block = line.strip().lstrip('#').strip()
            public_names[current_block] = []
        elif current_block is not None:
            # Process AST nodes that belong to the current block
            for node in tree.body:
                if hasattr(node, 'lineno') and node.lineno == i + 1:  # Ensure the line number matches
                    if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                        public_names[current_block].append(node.name)
                    elif isinstance(node, ast.ClassDef) and not node.name.startswith('_'):
                        public_names[current_block].append(node.name)
                    elif isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and not target.id.startswith('_'):
                                public_names[current_block].append(target.id)

    return public_names


def _generate_import_statement(module_name, file_path):
    public_names = _extract_public_names(file_path)
    formatted_import = f"from {module_name} import (\n"

    for block, names in public_names.items():
        if names:
            formatted_import += f"    # {block}\n    " + ", ".join(names) + ",\n"

    formatted_import += ")"
    return formatted_import


def get_main_file_contents(template_file_path, utils_file_path):
    def process_line(line, **kwargs):
        if not line.startswith('# PLACEHOLDER '):
            return line

        to_format = line[len('# PLACEHOLDER '):].strip(' {}')
        if to_format in kwargs:
            return kwargs[to_format]

        return line

    with open(template_file_path, 'r') as file:
        lines = file.read().splitlines()

    imports = _generate_import_statement('adventofcode.src.utils', utils_file_path)
    template = '\n'.join([
        process_line(line, utils=imports)
        for line in lines
    ])

    return template + '\n'


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('year', type=int)
    p.add_argument('day', type=int)
    p.add_argument('--debug', action='store_true',
                   help='create template in ./tmp, whose content is emptied first')
    args = p.parse_args()

    root = Path(__file__).parent
    logging.info(f'creating template for year {args.year} day {args.day} with root {root}')

    logging.info(f'downloading input')
    input = get_aoc_input(args.year, args.day)

    logging.info(f'downloading description and extracting code blocks')
    code_blocks = get_aoc_code_blocks(args.year, args.day)

    if args.debug:
        # set logging to debug
        logging.getLogger().setLevel(logging.DEBUG)
        root = root.joinpath('tmp')
        logging.debug(f'debug mode enabled, changing root to {root}')
        logging.debug('emptying root')
        empty_folder(root)

    logging.info('creating template...')
    folder = root.joinpath('src', str(args.year), str(args.day))
    folder.mkdir(parents=True)

    with folder.joinpath('input.txt').open('wt') as fh:
        fh.write(input)

    with folder.joinpath('examples.txt').open('wt') as fh:
        fh.write(EXAMPLES_SEPARATOR.join(code_blocks))

    # Write the main.py file
    main_file_path = folder.joinpath('main.py')
    utils_file_path = Path(__file__).parent.joinpath('src', 'utils.py')
    template_file_path = utils_file_path.parent.joinpath('template.py')
    with main_file_path.open('wt') as fh:
        fh.write(get_main_file_contents(template_file_path, utils_file_path))

