import numpy as np

from utils import *

Point = tuple[int, int]


def build_graph(grid: np.ndarray, start) -> dict[Point, set[Point]]:
    Q = {(start, None)}
    graph: dict[Point, set[Point]] = {}
    while len(Q) > 0:
        pos, prev = Q.pop()
        neigh = set(iter_path_tiles(grid, pos))
        neigh.difference_update([prev])
        # add edges
        graph[pos] = neigh

        for npos in neigh:
            if npos not in graph:
                Q.add((npos, pos))

    return graph


def print_graph(grid: np.ndarray, graph: dict[Point, set[Point]], start):
    grid = grid.copy()
    grid[start] = 'S'
    char_map = {
        lst[0]: char
        for char, lst in NEXT_MOVES.items()
        if len(lst) == 1
    }
    for u, vs in graph.items():
        if len(vs) == 1:
            v = next(iter(vs))
            delta = tuple(np.array(v) - u)
            grid[u] = char_map[delta]
        elif len(vs) == 0:
            grid[u] = 'E'
        else:
            grid[u] = '*'

    lines = [''.join(line) for line in grid]
    print('\n'.join(lines))


def shortest_path(graph: dict[Point, set[Point]], start: Point, w: int = 1):
    dist = {
        node: float('inf')
        for node in graph
    }
    prev = {
        node: None
        for node in graph
    }
    dist[start] = 0

    edges = [
        (src, dst)
        for src, lst in graph.items()
        for dst in lst
    ]
    for _ in range(len(graph)-1):
        for u, v in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

    # check for neg-weight cycle
    for u, v in edges:
        if dist[u] + w < dist[v]:
            prev[v] = u
            # a neg weight cycle exists; find a vertex on cycle
            visited = {
                node: False
                for node in graph
            }
            visited[v] = True
            while not visited[u]:
                visited[u] = True
                u = prev[u]
            # u is vertex on a neg cycle, find cycle itself
            ncycle = [u]
            v = prev[u]
            while v != u:
                ncycle.append(v)
                v = prev[v]
            raise ValueError(f'found neg cycle: {ncycle}')

    return dist, prev


grid = parse_data(load_data())
start = find_start(grid)
graph = build_graph(grid, start)
print_graph(grid, graph, start)
dist, prev = shortest_path(graph, start, w=-1)
