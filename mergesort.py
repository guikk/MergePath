def _innerMergeSort(arr, l, r, mergeFunc):

    if l < r:
        m = l+(r-l)//2
 
        _innerMergeSort(arr, l, m, mergeFunc)
        _innerMergeSort(arr, m+1, r, mergeFunc)
        mergeFunc(arr, l, m, r)

def mergeSort(arr, mergeFunc):
    return _innerMergeSort(arr, 0, len(arr)-1, mergeFunc)