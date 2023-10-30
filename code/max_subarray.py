import random
from math import inf as infinity
from typing import *


def max_subarray(numbers: List[int]) -> Tuple[int, int, int]:
    current_best = -infinity
    current_sum = 0
    start, end, i = 0, 0, 0
    for j in range(len(numbers)):
        x = numbers[j]
        current_sum = max(x, current_sum + x)
        if current_sum == x:
            i = j
        if current_sum > current_best:
            current_best = current_sum
            start = i
            end = j
    return start, end, current_best


def max_sum(numbers: List[int]) -> int:
    best_sum = -infinity
    current_sum = 0
    for x in numbers:
        current_sum = max(x, current_sum + x)
        best_sum = max(best_sum, current_sum)
    return best_sum


def main():
    numbers = [random.randint(-100, 100) for _ in range(1000)]
    start, end, total = max_subarray(numbers)
    actual = max_sum(numbers)
    assert actual == total and actual == sum(numbers[start:end + 1])


if __name__ == '__main__':
    main()
