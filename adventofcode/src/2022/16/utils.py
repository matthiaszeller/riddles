from pathlib import Path

import networkx as nx


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str):
    def parse_line(line: str):
        left, right = line.split(';')
        left = left.split()
        valve = left[1]
        rate = int(left[-1].split('=')[-1])
        tunnels = right.split('valve')[1].strip(' s').split(', ')
        return valve, rate, tunnels

    return list(map(parse_line, data.splitlines()))


def build_graph(data, start: str = 'AA', prune: bool = True):
    """
    Build a graph where each valve is connected to all other valves,
    tunnels are replaced by edges, and each node reflects the opening of a valve.

    """
    # This graph only accounts for time lost in tunnels
    G = nx.Graph()
    for src, _, lst in data:
        for dst in lst:
            G.add_edge(src, dst, w=1)
    # Add start
    G.add_edge('Start', start, w=0)

    # we just count cost of tunnels for now
    lengths = nx.shortest_path_length(G, weight='w')
    # build another graph to account for valve opening
    Gout = nx.Graph()
    for src, dst_length in lengths:
        for dst, length in dst_length.items():
            if length == 0:
                continue

            w = length + 1  # add 1 to account for valve opening
            Gout.add_edge(src, dst, w=w)

    # Add flow rate
    nx.set_node_attributes(Gout, 0, 'rate')
    for node, flow, _ in data:
        Gout.nodes[node]['rate'] = flow
        # Prune nodes with zero flow
        if prune and flow == 0:
            Gout.remove_node(node)

    # Add starting edge (was lost because Start to `start` has weight 0)
    if start in Gout.nodes:
        Gout.add_edge('Start', start, w=1)

    return Gout


class TreeNode:

    def __init__(self, src: str, dst: str, remaining_time: int, flow_rate: int, parent: 'TreeNode' = None):
        self.src = src
        self.dst = dst
        self.remaining_time = remaining_time
        self.parent = parent
        self.flow_rate: int = flow_rate
        self._total_pressure_release: int = -1

    @property
    def total_pressure_release(self) -> int:
        if self._total_pressure_release < 0:
            self_pressure_release = self.remaining_time * self.flow_rate
            parent_total = 0 if self.parent is None else self.parent.total_pressure_release
            self._total_pressure_release = self_pressure_release + parent_total

        return self._total_pressure_release

    def get_children(self, graph: nx.Graph):
        if self.remaining_time <= 0:
            return

        for next_node, edge_attrs in graph[self.dst].items():
            t = self.remaining_time - edge_attrs['w']
            if t < 0:
                continue

            if self.has_parent(next_node):
                continue

            dst_flow_rate = graph.nodes[next_node]['rate']
            tree_node = TreeNode(src=self.dst, dst=next_node, remaining_time=t, parent=self, flow_rate=dst_flow_rate)
            yield tree_node

    def has_parent(self, node: str) -> bool:
        current = self
        while current is not None:
            if current.dst == node:
                return True

            current = current.parent

        return False

    def __str__(self):
        current = self
        repr = []
        while current is not None:
            repr.append(f'{current.dst}')
            current = current.parent

        return ' <- '.join(repr)

    def __repr__(self):
        return f'TreeNode({self.src}-{self.dst}, t={self.remaining_time})'


example = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
