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
            print(f"Merging {self.A} and {self.B} sequentially")
            mergeByLength(
                self.S, self.startS,
                self.A, 0,
                self.B, 0,
                len(self.A) + len(self.B)
            )
            print(f"\tResult: {self.S[self.startS:self.startS+len(self.A)+len(self.B)+1]}")
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
        
        print(f"\tResult: {self.S[self.startS:self.startS+len(self.A)+len(self.B)+1]}")

    def M(self, i: int, j: int) -> bool:
        """
        Compute merge matrix element
        • (i and j are 1-indexed)
        """

        if i <= 0 or j > len(self.B):
            return False # out of bounds up right

        if j <= 0 or i > len(self.A):
            return True # out of bounds down left

        return self.A[i-1] > self.B[j-1]

    def findIntersection(self, diagonalIndex: int) -> Tuple[int,int]:
        """
        Compute point where the merge path crosses the ith diagonal
        """

        if diagonalIndex == 0:
            return (0, 0)

        diag = (diagonalIndex + 1) * self.segmentLength
        atop = len(self.A) if diag > len(self.A) else diag
        btop = diag - len(self.A) if diag > len(self.A) else 0
        abottom = btop

        while True:
            offset = (atop - abottom) // 2
            ai = atop - offset
            bi = btop + offset
            if self.M(ai,bi-1):
                if not self.M(ai-1,bi):
                    return (ai, bi)
                else:
                    atop = ai - 1
                    btop = bi + 1
            else:
                abottom = ai + 1

def parallelMerge(arr: List[int], l: int, m: int, r: int) -> None:
    pm = ParallelMerger(DEFAULT_THREADS, arr, l, m, r)
    pm.compute()