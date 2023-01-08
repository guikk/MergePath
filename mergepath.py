from typing import List, Tuple
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
        self.p = threads
        self.A = array[left:mid+1]
        self.B = array[mid+1:right+1]
        self.S = array
        self.startS = left
        self.segmentLength = (len(self.A) + len(self.B)) // self.p

    def compute(self) -> None:
        """
        • Divide work for p threads\n
        • Call delayed functions\n
        • Compute the final result affecting the input array
        """

        # TODO: Fix bug in diagonal choice, list items are being duplicated
        if self.segmentLength < 2:
            print(f"Merging {self.A} and {self.B} sequentially")
            mergeByLength(
                self.S, self.startS,
                self.A, 0,
                self.B, 0,
                len(self.A) + len(self.B)
            )
            print(f"\tResult: {self.S[self.startS:self.startS+len(self.A)+len(self.B)]}")
            return

        print(f"Merging {self.A} and {self.B} in {self.p} threads")
        for i in range(self.p):
            si = self.startS + i * self.segmentLength
            ai, bi = self.findIntersection(i)
            print(f"Thread {i} - (ai={ai},bi={bi}) - si={si}")
            mergeByLength(
                self.S, si,
                self.A, ai,
                self.B, bi,
                self.segmentLength
            )
        
        print(f"\tResult: {self.S[self.startS:self.startS+len(self.A)+len(self.B)]}")

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
        if i == 0:
            return (0, 0)

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