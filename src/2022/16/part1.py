from time import time

from utils import *


# --------- Initial thoughts
# Reminds of the 0-1 knapsack, but here the value is dynamic + constraint on items that can be selected
# based on already-selected items
# Also similar to prize-collecting traveling salesman

# --------- Strategy
# For the example, we can afford using bruteforce. The idea is to build a tree where each node
# represents a decision, and the leaves are possible solutions given the time constraint T=30min.
# In order to build the tree, we first create a graph G:
#   * a node XX in the graph represents opening valve XX
#   * a vertex XX-YY represents taking tunnel(s) from XX to YY
# a node in the graph is connected to every other node, their edge weight is adapted accordingly,
# accounting for both the traveling through (possibly several) tunnels and opening the valve.
#
# The resulting tree in for the example data has ~ 1.1M leaves, solution takes 11s.
#
# --------- Needed improvement for scaling
# Heuristic: the problem data has a LOT of zero flow-rate valves
# The *TRICK* now is to notice that we create the tree from a pruned graph G:
# we remove all nodes XX with flow rate 0, as opening this valve will never lead to a better solution,
# while the structure of the graph still accounts for tunnels connecting valve XX.
#
# Improvement for example data: 720 leaves in 10ms !!!
# For the problem data: 215k leaves in 1.6s


def build_tree(G: nx.Graph, T: int = 30, start: str = 'Start'):
    root = TreeNode(src='', dst=start, remaining_time=T, flow_rate=0)
    queue = [root]
    leaves: list[TreeNode] = []
    while len(queue) > 0:
        tree_node = queue.pop()
        children = list(tree_node.get_children(G))
        if len(children) == 0:
            leaves.append(tree_node)
        queue.extend(children)

    return leaves


data = parse_data(example)
t = time()
G = build_graph(data)
print(G)
leaves = build_tree(G)
print(len(leaves), 'leaves')
sol = max(leaves, key=lambda e: e.total_pressure_release)
t = time() - t
print(sol)
print(sol.total_pressure_release)
print(f'solution in {t:.4} s')
