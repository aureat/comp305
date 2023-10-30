import random
import math
from typing import *


def floor_sqrt(u: int) -> int:
    return math.floor(math.sqrt(u))


def ceil_sqrt(u: int) -> int:
    return math.ceil(math.sqrt(u))


class VEB:
    u: int
    min: Optional[int]
    max: Optional[int]
    clusters: Optional['List[VEB]']
    summary: Optional['VEB']

    def __init__(self, u: int):
        self.u = u
        self.min = None
        self.max = None
        if u > 2:
            self.clusters = [VEB(floor_sqrt(u)) for _ in range(ceil_sqrt(u))]
            self.summary = VEB(ceil_sqrt(u))

    def cluster_of(self, x: int) -> 'VEB':
        return self.clusters[self.high(x)]

    def cluster(self, i: int) -> 'VEB':
        return self.clusters[i]

    def contains(self, x):
        if x in [self.min, self.max]:
            return True
        elif self.u == 2:
            return False
        else:
            return self.cluster_of(x).contains(self.low(x))

    def insert(self, x):
        # if tree is empty, insertion is trivial
        if self.min is None:
            self.min = x
            self.max = x
            return

        # if x is less than min, swap x and min
        if x < self.min:
            self.min, x = x, self.min

        # insert x into appropriate cluster
        if self.u > 2 and self.cluster_of(x).min is None:
            self.summary.insert(self.high(x))
            self.cluster_of(x).insert(self.low(x))
        elif self.u > 2:
            self.cluster_of(x).insert(self.low(x))

        # update max
        if x > self.max:
            self.max = x

    def remove(self, x):
        # if tree has one element, empty tree
        if self.min == self.max:
            self.min = None
            self.max = None

        # if tree has two elements, delete x
        elif self.u == 2:
            if x == 0:
                self.min = 1
            else:
                self.min = 0
            self.max = self.min

        # if x is min
        elif x == self.min


    def index(self, x: int, y: int) -> int:
        return x * floor_sqrt(self.u) + y

    def high(self, x: int) -> int:
        return x // floor_sqrt(self.u)

    def low(self, x: int) -> int:
        return x % floor_sqrt(self.u)


def main():
    u = 2 ** 16
    tree = VEB(u)
    for _ in range(100):
        x = random.randint(0, u)
        tree.insert(x)
        assert tree.contains(x)


if __name__ == '__main__':
    main()
