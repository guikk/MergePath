from typing import List

def merge(arr: List[int], l: int, m: int, r: int) -> None:
    mergeByLength(arr, l, arr[l:m+1], 0, arr[m+1:r+1], 0, r - l + 1)

def mergeByLength(
    S: List[int], si: int,
    A: List[int], ai: int,
    B: List[int], bi: int, 
    length: int
    ) -> None:
    """
    Merge the <length> smallest elements from arrays A and B into S\n
    The starting indexes for each array are ai, bi and si
    """
    
    count = 0
    
    while count < length and ai < len(A) and bi < len(B):
        if A[ai] <= B[bi]:
            S[si] = A[ai]
            ai += 1
        else:
            S[si] = B[bi]
            bi += 1
        si += 1
        count += 1

    while count < length and ai < len(A):
        S[si] = A[ai]
        ai += 1
        si += 1
        count += 1

    while count < length and bi < len(B):
        S[si] = B[bi]
        bi += 1
        si += 1
        count += 1