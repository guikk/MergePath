from typing import List, Tuple
import dask
from merge import mergeByLength

DEFAULT_THREADS = 4

class ParallelMerger:
    """
    Merges two adjacent ordered segments inside an array
    """
    def __init__(
        self, threads: int, array: List[int],
        left: int, mid: int, right: int
    ) -> None:
        self.tag = str((left,mid,right))
        self.p = threads
        self.A = array[left:mid+1]
        self.B = array[mid+1:right+1]
        self.S = array
        self.startS = left
        self.length = right - left + 1

    def compute(self) -> None:
        """
        • Divide work for p threads\n
        • Call delayed functions\n
        • Compute the final result affecting the input array
        """

        segmentLength = (self.length) // self.p

        if segmentLength < self.p:
            # print(f"Merging {self.A} and {self.B} sequentially")
            mergeByLength(
                self.S, self.startS,
                self.A, 0,
                self.B, 0,
                self.length
            )
            # print(f"\tResult: {self.S[self.startS:self.startS + self.length]}")
            return

        # print(f"({self.tag}) Merging {self.A} and {self.B} in {self.p} threads")
        @dask.delayed(nout=2)
        def findDiagonalIntersection(i: int):
            return self.findDiagonalIntersection(i)

        @dask.delayed(nout=0)
        def mergeSegment(si: int, ai: int, bi: int):
            mergeByLength(
                self.S, self.startS + si,
                self.A, ai,
                self.B, bi,
                segmentLength if i < self.p - 1 else self.length - si
            )

        results = []
        for i in range(self.p):
            si = i * segmentLength
            ai, bi  = findDiagonalIntersection(si)
            results.append(mergeSegment(si, ai, bi))

        dask.compute(results)
        # print(f"\tResult: {self.S[self.startS:self.startS+len(self.A)+len(self.B)]}")

    # TODO: Maybe refactor this function inside `findDiagonalIntersection`
    def M(self, i: int, j: int) -> bool:
        """
        Compute merge matrix element\n
        • Mij <=> A[i] > B[j]\n
        • When indexes are out of bounds the result is set 
        to True or False depending on the position
        """

        if i < 0 or j > len(self.B) - 1:
            return False # out of bounds up or right

        if j < 0 or i > len(self.A) - 1:
            return True # out of bounds down or left

        return self.A[i] > self.B[j]

    def findDiagonalIntersection(self, i: int) -> Tuple[int,int]:
        """
        Compute point where the merge path crosses the ith cross diagonal of the merge matrix.
        Intuition for this problem can be found in Proposition 13 of the Merge Path paper (p.5).\n
        (How many elements from A and B have been already taken after i steps of merging the two arrays?)
        """

        maxA = min(len(self.A), i)
        minA = max(i - len(self.B), 0)

        while minA < maxA:
            midA = minA + (maxA - minA) // 2
            # ai + bi == i is invariant in the cross diagonal
            ai, bi = midA, i - midA

            if not self.M(ai, bi - 1):
                # lower than intersection
                minA = midA + 1
                continue

            if self.M(ai - 1, bi):
                # higher than intersection
                maxA = midA - 1
                continue

            minA, maxA = midA, midA # midA is the solution

        return (minA, i - minA)
        
def parallelMerge(arr: List[int], l: int, m: int, r: int) -> None:
    pm = ParallelMerger(DEFAULT_THREADS, arr, l, m, r)
    pm.compute()