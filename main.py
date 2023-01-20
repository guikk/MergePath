from time import time
import numpy as np
import sys

from mergesort import mergeSort
from merge import merge
from mergepath import parallelMerge

sequentialSort = lambda arr: mergeSort(arr, merge)
parallelSort = lambda arr: mergeSort(arr, parallelMerge)

def main():
    inputSize = 1000
    if len(sys.argv) == 2:
        inputSize = int(sys.argv[1])
    input = list(np.random.randint(low=0, high=100, size=(inputSize)))

    arr = input.copy()
    print(f"\nInput size = {inputSize}")
    print(f"\nSequential\n")#  Input = {arr}")
    s = time()
    sequentialSort(arr)
    e = time()
    # print(f"  Output = {arr}")
    print(f"  Time = {(e-s):.8f}s")

    arr = input.copy()
    print(f"\nParallel\n")#  Input = {arr}")
    s = time()
    parallelSort(arr)
    e = time()
    # print(f"  Output = {arr}")
    print(f"  Time = {(e-s):.8f}s")


if __name__ == "__main__":
    main()