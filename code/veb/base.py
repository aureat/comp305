import random
import math
from typing import *


def fsqrt(u: int) -> int:
    return math.floor(math.sqrt(u))


def csqrt(u: int) -> int:
    return math.ceil(math.sqrt(u))


class VEB:
    u: int = 2
    min: Optional[int]
    max: Optional[int]
    clusters: Optional['List[VEB]']
    summary: Optional['VEB']

    def __init__(self, u: int):
        self.u = u
        self.min = None
        self.max = None
        if u > 2:
            self.clusters = [VEB(fsqrt(u)) for _ in range(csqrt(u))]
            self.summary = VEB(csqrt(u))
        else:
            self.clusters = None
            self.summary = None

    def cluster_of(self, x: int) -> 'VEB':
        return self.clusters[self.high(x)]

    def cluster(self, i: int) -> 'VEB':
        return self.clusters[i]

    def is_empty(self: 'VEB') -> bool:
        return self.min is None

    def contains(self: 'VEB', x: int) -> bool:
        if x in [self.min, self.max]:
            return True
        elif self.u == 2:
            return False
        else:
            return self.cluster_of(x).contains(self.low(x))

    def insert(self: 'VEB', x: int):
        # if tree is empty, insertion is trivial
        if self.is_empty():
            self.min = self.max = x
            return

        # if x is less than min, swap x and min
        if x < self.min:
            self.min, x = x, self.min

        # insert x into appropriate cluster
        if self.u > 2:
            # if cluster is empty, insert it into summary
            if self.cluster_of(x).min is None:
                self.summary.insert(self.high(x))
            self.cluster_of(x).insert(self.low(x))

        # update max
        if x > self.max:
            self.max = x

    def delete(self: 'VEB', x: int):
        # if tree has one element, empty tree
        if self.min == self.max:
            self.min = None
            self.max = None
            return

        # if tree has two elements, delete x
        # if x was min, set min to max, else set max to min
        if self.u == 2:
            self.min = 1 if x == 0 else 0
            self.max = self.min
            return

        # if x is min, it does not appear in any cluster
        # find minimum that DOES appear and replace x with that
        # then mark x so that it is deleted
        if x == self.min:
            first_cluster = self.summary.min
            x = self.index(first_cluster, self.cluster(first_cluster).min)
            self.min = x

        # delete x from appropriate cluster
        cluster = self.cluster_of(x)
        cluster.delete(self.low(x))

        # if cluster is empty, delete it from summary
        if cluster.is_empty():
            self.summary.delete(self.high(x))
            if x == self.max:
                summary_max = self.summary.max
                self.max = self.index(summary_max, self.cluster(summary_max).max) \
                    if summary_max is not None else self.min
            return

        # if x was max, replace it with the next max
        if x == self.max:
            self.max = self.index(self.high(x), self.cluster_of(x).max)

    def successor(self, x: int) -> Optional[int]:
        # if it's the base case, return either self.max or None
        if self.u == 2:
            if x == 0 and self.max == 1:
                return 1
            return None

        # if x is less than min, return min
        # min is a special case because it's not in the tree
        if self.min is not None and x < self.min:
            return self.min

        # if x is less than max of its cluster, find successor in cluster
        max_low = self.cluster_of(x).max
        if max_low is not None and self.low(x) < max_low:
            offset = self.cluster_of(x).successor(self.low(x))
            return self.index(self.high(x), offset)

        # otherwise look for a non-empty cluster in the summary
        succ_cluster = self.summary.successor(self.high(x))
        if succ_cluster is None:
            return None

        # if there is one, find the min of that cluster and return it
        offset = self.cluster(succ_cluster).min
        return self.index(succ_cluster, offset)

    def predecessor(self, x: int) -> Optional[int]:
        # if it's the base case, return either self.min or None
        if self.u == 2:
            if x == 1 and self.min == 0:
                return 0
            return None

        # if x is greater than max, return max
        if self.max is not None and x > self.max:
            return self.max

        # if x is greater than min of its cluster, find predecessor in cluster
        min_low = self.cluster_of(x).min
        if min_low is not None and self.low(x) > min_low:
            offset = self.cluster_of(x).predecessor(self.low(x))
            return self.index(self.high(x), offset)

        # otherwise look for a non-empty cluster in the summary
        pred_cluster = self.summary.predecessor(self.high(x))
        if pred_cluster is None:
            # min is a special case because it's not in the tree
            if self.min is not None and x > self.min:
                return self.min
            return None

        # if there is one, find the max of that cluster and return it
        offset = self.cluster(pred_cluster).max
        return self.index(pred_cluster, offset)

    def index(self, x: int, y: int) -> int:
        return x * fsqrt(self.u) + y

    def high(self, x: int) -> int:
        return x // fsqrt(self.u)

    def low(self, x: int) -> int:
        return x % fsqrt(self.u)


def main():
    u = 2 ** 16
    tree = VEB(u)
    for _ in range(100):
        x = random.randint(0, u)
        tree.insert(x)
        assert tree.contains(x)
        tree.delete(x)
        assert not tree.contains(x)


if __name__ == '__main__':
    main()
