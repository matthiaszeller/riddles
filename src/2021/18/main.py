from copy import deepcopy
from math import floor, ceil
from typing import Union, Literal
from functools import reduce as iter_reduce

from utils import *


class TreeNode:

    LR_MAPPING = {'0': 'left', '1': 'right'}

    def __init__(self, left: 'TreeNode' = None, right: 'TreeNode' = None, value: int = None,
                 parent: 'TreeNode' = None):
        self.left = left
        self.right = right
        self.value = value
        self.parent = parent
        self.depth = 0 if self.parent is None else self.parent.depth + 1

    @property
    def is_pair(self) -> bool:
        return self.value is None

    @property
    def is_root(self) -> bool:
        return self.parent is None

    def get_left_value(self) -> Union['TreeNode', None]:
        return self._get_value('left')

    def get_right_value(self) -> Union['TreeNode', None]:
        return self._get_value('right')

    def get_magnitude(self) -> int:
        if not self.is_pair:
            return self.value

        return self.left.get_magnitude() * 3 + self.right.get_magnitude() * 2

    def _get_value(self, lr: Literal['left', 'right']):
        if self.is_root:
            return None

        parent = self.parent
        previous = self
        while getattr(parent, lr) == previous:
            previous = parent
            parent = parent.parent
            if parent is None:
                return None

        # now, descend to the rightmost value
        node = getattr(parent, lr)
        rl = 'left' if lr == 'right' else 'right'
        while node.is_pair:
            node = getattr(node, rl)

        return node

    def explode(self):
        assert self.is_pair, 'cannot explode regular number'
        assert not self.left.is_pair and not self.right.is_pair, \
            'can only explode pairs whose elements are regular numbers'
        # add values
        if (left := self.get_left_value()) is not None:
            left.value += self.left.value
        if (right := self.get_right_value()) is not None:
            right.value += self.right.value
        # replace exploding pair with regular number 0
        self.left = None
        self.right = None
        self.value = 0

    def split(self):
        assert not self.is_pair, 'cannot split pairs'
        n = self.value / 2
        self.value = None
        self.left = TreeNode(parent=self, value=floor(n))
        self.right = TreeNode(parent=self, value=ceil(n))

    def add(self, other: Union[list, 'TreeNode']):
        if isinstance(other, list):
            other = TreeNode.from_list(other)

        parent = TreeNode(left=self, right=other)
        self.parent = parent
        other.parent = parent
        # adjust depths
        for node in self:
            node.depth += 1
        for node in other:
            node.depth += 1

        parent.reduce()
        return parent


    @classmethod
    def from_list(cls, lst: list):
        def inner(elem, parent: TreeNode):
            if isinstance(elem, int):
                return TreeNode(value=elem, parent=parent)

            node = TreeNode(parent=parent)
            node.left = inner(elem[0], parent=node)
            node.right = inner(elem[1], parent=node)
            return node

        node = TreeNode()
        node.left = inner(lst[0], node)
        node.right = inner(lst[1], node)
        return node

    def to_list(self) -> list | int:
        if not self.is_pair:
            return self.value

        return [self.left.to_list(), self.right.to_list()]

    @classmethod
    def from_string(cls, string: str):
        return cls.from_list(eval(string))

    def __repr__(self):
        return str(self.to_list())

    def __getitem__(self, item: str):
        current = self
        for i in item:
            attr = self.LR_MAPPING[i]
            current = getattr(current, attr)

        return current

    def __iter__(self):
        """DFS search with left before right"""
        q = [self]
        while len(q) > 0:
            item = q.pop()
            yield item

            if item.is_pair:
                q.append(item.right)
                q.append(item.left)

    def reduce(self):
        action = False
        for node in self:
            if node.depth >= 4 and node.is_pair:
                node.explode()
                action = True
                break

        if action:
            self.reduce()
            return

        for node in self:
            if not node.is_pair and node.value >= 10:
                node.split()
                self.reduce()
                action = True
                break

        if action:
            self.reduce()


examples = """[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"""

for example in examples.splitlines():
    root = TreeNode.from_string(example)
    assert example == str(root).replace(' ', '')


r = TreeNode.from_string('[[1,9],[8,5]]')
print(r)
for e in (r.left.left, r.left.right, r.right.left):
    print(f'left value of {e}: {e.get_left_value()}; right value of {e}: {e.get_right_value()}')


for start, id, expected in [
    ([[[[[9,8],1],2],3],4], '0000', [[[[0,9],2],3],4]),
    ([7,[6,[5,[4,[3,2]]]]], '1111', [7,[6,[5,[7,0]]]]),
    ([[6,[5,[4,[3,2]]]],1], '0111', [[6,[5,[7,0]]],3]),
    ([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], '0111', [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
]:
    r = TreeNode.from_list(start)
    r[id].explode()
    assert r.to_list() == expected


left = TreeNode.from_list([[[[4,3],4],4],[7,[[8,4],9]]])
right = [1, 1]
expected = [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
assert left.add(right).to_list() == expected


def add_numbers(listed: str):
    numbers = map(TreeNode.from_string, listed.splitlines())
    final = iter_reduce(lambda acc, e: acc.add(e), numbers)
    return final


examples = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
final = add_numbers(examples)
assert final.to_list() == [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]


examples = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
final = add_numbers(examples)
assert final.to_list() == [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
assert final.get_magnitude() == 4140


final = add_numbers(load_data())
print(final)
print(final.get_magnitude())


# ======================= PART 2
print('\n' * 5)

def find_pair_largest_magnitude(numbers: list[TreeNode]):
    magn = float('-inf')
    optimal = None
    for i in range(len(numbers)):
        for j in range(i+1, len(numbers)):
            for left, right in [(i, j), (j, i)]:
                result = deepcopy(numbers[left]).add(deepcopy(numbers[right])).get_magnitude()
                if result > magn:
                    magn = result
                    optimal = left, right

    left, right = optimal
    print(f'pair with largest magnitude {magn} {(left, right)}')
    print(f'left  = {numbers[left]}')
    print(f'right = {numbers[right]}')
    final = deepcopy(numbers[left]).add(deepcopy(numbers[right]))
    print(final)

    return optimal


numbers = list(map(TreeNode.from_string, examples.splitlines()))
find_pair_largest_magnitude(numbers)

numbers = list(map(TreeNode.from_string, load_data().splitlines()))
find_pair_largest_magnitude(numbers)
