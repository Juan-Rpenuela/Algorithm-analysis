"""Sorting algorithm implementations with types and docstrings.

Each public function accepts a sequence of comparable items and returns a
new list with the items in non-decreasing order (functions do not sort
in-place to avoid surprising side-effects in tests/experiments).

Complexities (informative):
- bubble_sort: O(n^2) time, O(1) extra space
- insertion_sort: O(n^2) time (best O(n)), O(1) extra space
- merge_sort: O(n log n) time, O(n) extra space (stable)
- quick_sort: average O(n log n), worst O(n^2); recursion extra space
- python_sort: Timsort (stable), O(n log n) time

The implementations aim to be clear and easy to test rather than the
most optimized possible versions.
"""

from typing import List, Sequence, TypeVar

T = TypeVar("T")


def bubble_sort(arr: Sequence[T]) -> List[T]:
    """Return a new list sorted by bubble sort.

    Not in-place: a copy is returned. Stable for equal elements.
    Time complexity: O(n^2) average/worst, O(n) best (already sorted).
    """
    a: List[T] = list(arr)
    n = len(a)
    # Bubble sort repeatedly steps through the list, comparing adjacent
    # elements and swapping them if they are in the wrong order. Each pass
    # moves the next-largest element to its final position (like bubbles rising).
    #
    # Time complexity:
    # - Worst/average: O(n^2) because of the nested loops (roughly n*(n-1)/2 comparisons).
    # - Best: O(n) when the input is already sorted and we detect no swaps.
    # Space complexity: O(n) additional for the returned copy, O(1) extra in-place.
    # Stability: stable (equal elements preserve relative order).
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            # No swaps means the list is already sorted.
            break
    return a


def insertion_sort(arr: Sequence[T]) -> List[T]:
    """Return a new list sorted by insertion sort.

    Not in-place: a copy is returned. Stable algorithm.
    Time complexity: O(n^2) average/worst.
    """
    a: List[T] = list(arr)
    # Insertion sort builds the sorted portion of the list one element at a time.
    # For each new element we shift larger items to the right and insert the
    # element in the correct spot. Efficient for nearly-sorted data.
    #
    # Time complexity:
    # - Worst/average: O(n^2) due to shifting elements (e.g., reversed input).
    # - Best: O(n) when the input is already (or nearly) sorted — minimal shifts.
    # Space complexity: O(n) for returned copy, O(1) extra.
    # Stability: stable.
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr: Sequence[T]) -> List[T]:
    """Return a new list sorted by merge sort (stable).

    Time complexity: O(n log n).
    """
    if len(arr) <= 1:
        return list(arr)

    # Merge sort divides the list, sorts each half recursively, and merges
    # the two sorted halves. The merge step runs in linear time relative to
    # the sum of the lengths of the halves.
    #
    # Time complexity: O(n log n) in all cases because we perform O(log n)
    # levels of division and O(n) work per level to merge.
    # Space complexity: O(n) additional space for merging (not in-place).
    # Stability: stable (merge preserves original order of equal elements).
    def _merge(left: List[T], right: List[T]) -> List[T]:
        i = j = 0
        out: List[T] = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
        out.extend(left[i:])
        out.extend(right[j:])
        return out

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def quick_sort(arr: Sequence[T]) -> List[T]:
    """Return a new list sorted by quick sort (functional style).

    This implementation favors clarity over in-place performance. Worst-case
    time is O(n^2) for pathological pivot choices.
    """
    a: List[T] = list(arr)
    # Quick sort picks a pivot and partitions the input into elements less
    # than, equal to, and greater than the pivot, then recursively sorts
    # the partitions. The average-case performs well, but poor pivot choices
    # (e.g., already sorted input with bad pivot) can trigger worst-case
    # quadratic behavior.
    #
    # Time complexity:
    # - Average: O(n log n) when partitions are reasonably balanced.
    # - Worst: O(n^2) when partitions are highly unbalanced every recursion.
    # Space complexity: O(log n) average recursion depth (O(n) worst-case).
    # Stability: this simple partitioning is not stable (relative order of
    # equal elements may change).
    if len(a) <= 1:
        return a
    pivot = a[len(a) // 2]
    left = [x for x in a if x < pivot]
    middle = [x for x in a if x == pivot]
    right = [x for x in a if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def python_sort(arr: Sequence[T]) -> List[T]:
    """Return a new list using Python's built-in `sorted` (Timsort).

    Stable and generally the best choice for real workloads.
    """
    return sorted(arr)
