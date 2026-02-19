# Algorithm Analysis — Sorting Algorithm Comparison

This repository compares five sorting algorithms experimentally and plots execution time vs input size.

Implemented algorithms (summary and Big-O):

- `bubble_sort` — simple comparison sort that repeatedly swaps adjacent
	out-of-order elements. Big-O: best O(n), average/worst O(n^2). Stable.

- `insertion_sort` — builds a sorted prefix by inserting items one-by-one;
	efficient on small or nearly-sorted inputs. Big-O: best O(n), average/worst O(n^2). Stable.

- `merge_sort` — divide-and-conquer stable sort that splits, sorts, and
	merges halves. Big-O: O(n log n) time in all cases, O(n) extra space.

- `quick_sort` — pivot-based partitioning sort; typically fast in
	practice. Big-O: average O(n log n), worst O(n^2) (bad pivots). Not
	stable without modifications.

- `python_sort` — wrapper for Python's `sorted()` which uses Timsort;
	stable and optimized for real-world data. Big-O: O(n log n) average/worst.

Run experiments:

```
python experiments/experiment.py
```

Run tests:

```
pip install -r requirements.txt
pytest -q
```

Plot saved to `experiments/plots/complexity.png`.
