from pathlib import Path

example = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def load_data():
    return Path(__file__).parent.joinpath('data.txt').read_text()


def sort_ranges_by_src(ranges: list[tuple[int, int, int]]):
    ranges.sort(key=lambda rng: rng[1])


def parse_data(data: str):
    def process_nums(line: str) -> list[int]:
        return list(map(int, line.strip().split()))

    def process_map(section: str):
        desc, rest = section.split(maxsplit=1)
        desc = desc.split(' ')[0].split('-')
        source, dest = desc[0], desc[2]
        ranges = [
            tuple(process_nums(line))
            for line in rest.splitlines()[1:]
        ]
        return source, dest, ranges

    sections = data.split('\n\n')
    seeds: list[int] = process_nums(sections[0].split(':')[1])

    chain: list[str] = ['seed']
    maps: dict[tuple[str, str], list[tuple[int]]] = {}
    for i, section in enumerate(sections[1:]):
        source, dest, ranges = process_map(section)
        assert chain[i] == source
        chain.append(dest)
        sort_ranges_by_src(ranges)
        maps[(source, dest)] = ranges

    return seeds, chain, maps
