import random
from typing import Callable, List

from algorithms.sorting import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    python_sort,
)


def random_list(n: int, seed: int = 0) -> List[int]:
    random.seed(seed)
    return [random.randint(-1000, 1000) for _ in range(n)]


def check_all_equal(arr: List[int]):
    expected = sorted(arr)
    algos: List[Callable[[List[int]], List[int]]] = [
        bubble_sort,
        insertion_sort,
        merge_sort,
        quick_sort,
        python_sort,
    ]
    for f in algos:
        result = f(arr)
        assert result == expected


def test_empty():
    check_all_equal([])


def test_single():
    check_all_equal([1])


def test_small_random():
    arr = random_list(50)
    check_all_equal(arr)


def test_with_duplicates():
    arr = [5, 1, 3, 5, 2, 1, 4]
    check_all_equal(arr)


def test_already_sorted():
    arr = list(range(20))
    check_all_equal(arr)


def test_reversed():
    arr = list(range(20, 0, -1))
    check_all_equal(arr)


def test_original_unchanged():
    arr = [3, 2, 1]
    original = list(arr)
    _ = bubble_sort(arr)
    _ = insertion_sort(arr)
    _ = merge_sort(arr)
    _ = quick_sort(arr)
    _ = python_sort(arr)
    assert arr == original


def test_medium_random_performance():
    # sanity check for larger input (keeps CI reasonably fast)
    arr = random_list(200, seed=1)
    check_all_equal(arr)
