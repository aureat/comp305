from typing import *
from mwis.tree import *


def include(node: Node, path: Set[Node]) -> Tuple[int, Set[Node]]:
    current_path = path.copy()
    current_path.add(node)
    current_total = profit(node)
    if node.m_include is not None:
        return node.m_include, current_path
    new_include(node)
    for child in children(node):
        (temp_total, temp_path) = exclude(child, current_path)
        current_total += temp_total
        current_path = current_path.union(temp_path)
    node.m_include = current_total
    return current_total, current_path


def exclude(node: Node, path: Set[Node]) -> Tuple[int, Set[Node]]:
    current_path = path.copy()
    current_total = 0
    if node.m_exclude is not None:
        return node.m_exclude, current_path
    new_exclude(node)
    for child in children(node):
        (total1, path1) = include(child, current_path)
        (total2, path2) = exclude(child, current_path)
        max_total = max(total1, total2)
        max_path = path1 if max_total == total1 else path2
        current_path = current_path.union(max_path)
        current_total += max_total
    node.m_exclude = current_total
    return current_total, current_path


def main():
    root: Node = Node.A
    (include_total, include_path) = include(root, set())
    (exclude_total, exclude_path) = exclude(root, set())
    max_total = max(include_total, exclude_total)
    max_path = include_path if max_total == include_total else exclude_path
    max_path = sorted(max_path, key=lambda x: x.value)
    print("Max total:", max_total)
    print("Max path:", max_path)
    print("Counts:", num_calls)
    includes = sum([x[0] for x in num_calls.values()])
    excludes = sum([x[1] for x in num_calls.values()])
    print("Includes:", includes)
    print("Excludes:", excludes)

    print("\nMemoization Table:")
    for node in Node.__iter__():
        print(node, cached_include[node], cached_exclude[node])


if __name__ == '__main__':
    main()
