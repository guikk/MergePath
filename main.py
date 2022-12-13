from time import time
import numpy as np

from mergesort import mergeSort
from merge import merge
from mergepath import parallelMerge

sequentialSort = lambda arr: mergeSort(arr, merge)
parallelSort = lambda arr: mergeSort(arr, parallelMerge)

def main():
    input = list(np.random.randint(low=0, high=100, size=(30)))

    arr = input.copy()
    print(f"\nSequential\n  Input = {arr}")
    s = time()
    sequentialSort(arr)
    e = time()
    print(f"  Output = {arr}")
    print(f"  Time = {10**6 * (e-s):.0f}μs")

    arr = input.copy()
    print(f"\nParallel\n  Input = {arr}")
    s = time()
    parallelSort(arr)
    e = time()
    print(f"  Output = {arr}")
    print(f"  Time = {10**6 * (e-s):.0f}μs")


if __name__ == "__main__":
    main()