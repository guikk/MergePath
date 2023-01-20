from typing import List, Tuple
import dask
from merge import mergeByLength
from time import time

DEFAULT_THREADS = 4
MIN_PAR_PROBLEM = 2 ** 10

# TODO: Maybe refactor this function inside `findDiagonalIntersection`
def mergeMatrix(A: List[int], B: List[int], i: int, j: int) -> bool:
    """
    Compute merge matrix element\n
    • Mij <=> A[i] > B[j]\n
    • When indexes are out of bounds the result is set 
    to True or False depending on the position
    """

    if i < 0 or j > len(B) - 1:
        return False # out of bounds up or right

    if j < 0 or i > len(A) - 1:
        return True # out of bounds down or left

    return A[i] > B[j]

@dask.delayed(nout=2)
def findDiagonalIntersection(A: List[int], B: List[int], i: int) -> Tuple[int,int]:
    """
    Compute point where the merge path crosses the ith cross diagonal of the merge matrix.
    Intuition for this problem can be found in Proposition 13 of the Merge Path paper (p.5).\n
    (How many elements from A and B have been already taken after i steps of merging the two arrays?)
    """

    maxA = min(len(A), i)
    minA = max(i - len(B), 0)

    while minA < maxA:
        midA = minA + (maxA - minA) // 2
        # ai + bi == i is invariant in the cross diagonal
        ai, bi = midA, i - midA

        if not mergeMatrix(A, B, ai, bi - 1):
            # lower than intersection
            minA = midA + 1
            continue

        if mergeMatrix(A, B, ai - 1, bi):
            # higher than intersection
            maxA = midA - 1
            continue

        minA, maxA = midA, midA # midA is the solution

    return (minA, i - minA)
        
def parallelMerge(arr: List[int], l: int, m: int, r: int) -> None:
    """
    Merges two adjacent ordered segments inside an array
    """
    p = DEFAULT_THREADS
    A = arr[l:m+1]
    B = arr[m+1:r+1]
    S = arr
    startS = l
    length = r - l + 1

    if length < MIN_PAR_PROBLEM:
        mergeByLength(S, startS, A, 0, B, 0, length)
        return

    """
    • Divide work for p threads\n
    • Call delayed functions\n
    • Compute the final result affecting the input array
    """
    @dask.delayed(nout=0)
    def merge(si, ai, bi, l):
        mergeByLength(S, si, A, ai, B, bi, l)

    segmentLength = (length) // p

    def buildTasks():
        for i in range(p):
            si = i * segmentLength
            ai, bi = findDiagonalIntersection(A, B, si)
            yield merge(
                startS + si, ai, bi, 
                segmentLength if i < p - 1 else length - si
            )

    dask.compute(buildTasks())
