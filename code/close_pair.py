import math
import random
from typing import *

Location = Tuple[float, float]
Pair = Tuple[Location, Location] | None


def close(a: Location, b: Location) -> bool:
    return math.dist(a, b) <= 1


def close_pair_iterative(lx: List[Location], ly: List[Location]) -> Pair:
    for i in range(1, len(lx) - 1):
        if close(px := lx[i], px_prev := lx[i - 1]):
            return px_prev, px
        if close(px := lx[i], px_next := lx[i + 1]):
            return px_prev, px
        if (j := ly.index(px)) > 0 and close(px, ly[j - 1]):
            return px, ly[j - 1]
        if j < len(lx) - 1 and close(px, ly[j + 1]):
            return px, ly[j + 1]


def close_pair(lx: List[Location], ly: List[Location]) -> Pair:
    if len(lx) == 2 and close(lx[0], lx[1]):
        return lx[0], lx[1]
    elif len(lx) < 2:
        return None

    mid = len(lx) // 2

    lx_left = lx[:mid]
    ly_left = list(filter(lambda p: p in lx_left, ly))
    if (result := close_pair(lx_left, ly_left)) is not None:
        return result

    lx_right = lx[mid:]
    ly_right = list(filter(lambda p: p in lx_right, ly))
    if (result := close_pair(lx_right, ly_right)) is not None:
        return result

    # iterate from mid to left and right to find a pair that is too close
    

def main():
    N = 10
    nums = [(round(random.random() * 10, 4), round(random.random() * 10, 4)) for _ in range(N)]
    lx, ly = sorted(nums, key=lambda x: x[0]), sorted(nums, key=lambda x: x[1])

    print("Points:", lx)
    close_pairs = set([(p1, p2, math.dist(p1, p2)) for p1 in lx for p2 in lx if p1 != p2 and math.dist(p1, p2) <= 1])
    print("Actual solution:", actual := close_pairs)

    # print("Iterative solution:", iterative := close_pair_iterative(lx, ly))
    # print("Iterative correct?", actual in iterative)

    recursive = close_pair(lx, ly)
    if recursive is None:
        print("Recursive solution:", recursive)
        print("Recursive correct?", len(actual) == 0)
    else:
        p1, p2 = recursive
        print("Recursive solution:", recursive)
        print("Recursive distance:", math.dist(p1, p2))
        print("Recursive correct?", recursive in actual)


if __name__ == '__main__':
    main()
