DEFAULT_THREADS = 4

class ParallelMerger:
    """
    In-place parallel merger of two adjacent segments of one array
    """
    def __init__(self, threads, array, left, mid, right):
        self.p = threads
        self.A = array[left:mid+1]
        self.B = array[mid+1:right+1]
        self.S = array
        self.segmentLength = (len(self.A) + len(self.B)) // self.p

    def compute(self):
        for i in range(self.p):
            si = i * self.segmentLength + 1
            ai, bi = self.findIntersection(i)
            self.merge(ai, bi, si, self.segmentLength)


    def merge(self, ai, bi, si, length):
        pass

    def M(self, i, j):
        """
        Compute merge matrix element
        • i and j are 1-indexed
        """

        if i == 0 or j > len(self.B):
            return False # out of bounds up right

        if j == 0 or i > len(self.A):
            return True # out of bounds down left

        return self.A[i-1] > self.B[j-1]

    def findIntersection(self, diagonalIndex):
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

def parallelMerge(arr, l, m, r):
    pm = ParallelMerger(DEFAULT_THREADS, arr, l, m, r)
    pm.compute()