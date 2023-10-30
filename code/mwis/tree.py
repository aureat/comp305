from enum import Enum, auto
from typing import *


cached_include = {}
cached_exclude = {}


class Node(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()
    H = auto()
    I = auto()
    J = auto()
    K = auto()
    L = auto()
    M = auto()
    N = auto()
    O = auto()

    @property
    def m_include(self):
        m = cached_include.get(self, None)
        cached_include[self] = m
        return m

    @m_include.setter
    def m_include(self, value):
        cached_include[self] = value

    @property
    def m_exclude(self):
        m = cached_exclude.get(self, None)
        cached_exclude[self] = m
        return m

    @m_exclude.setter
    def m_exclude(self, value):
        cached_exclude[self] = value

    def __repr__(self):
        return self.name


tree = {
    Node.A: [Node.B, Node.C, Node.D],
    Node.B: [Node.E, Node.F],
    Node.C: [Node.G, Node.H, Node.I],
    Node.D: [Node.J, Node.K],
    Node.H: [Node.L, Node.M, Node.N],
    Node.J: [Node.O],
}

weights = {
    Node.A: 6,
    Node.B: 4,
    Node.C: 8,
    Node.D: 8,
    Node.E: 5,
    Node.F: 6,
    Node.G: 2,
    Node.H: 8,
    Node.I: 3,
    Node.J: 9,
    Node.K: 7,
    Node.L: 5,
    Node.M: 4,
    Node.N: 6,
    Node.O: 2,
}


def children(node: Node) -> List[Node]:
    return tree.get(node, [])


def profit(node: Node) -> int:
    return weights.get(node)


num_calls = {}


def new_include(node: Node):
    (inc, exc) = num_calls.get(node, (0, 0))
    num_calls[node] = (inc + 1, exc)


def new_exclude(node: Node):
    (inc, exc) = num_calls.get(node, (0, 0))
    num_calls[node] = (inc, exc + 1)
