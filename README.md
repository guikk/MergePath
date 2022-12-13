Distributed programming project for the Advanced Parallel Systems course at Grenoble INP - Ensimag 

# Merge Path
Python implementation using the [`dask`](https://www.dask.org/) library for parallelization.

The goal of the project is to compare the performance of parallel merging with sequential merging in the merge sort algorithm.

### Reference Paper
📄[Merge Path - A Visually Intuitive Approach to Parallel Merging](https://arxiv.org/pdf/1406.2628.pdf)

👨‍🔬Oded Green 🧑‍🔬Saher Odehb 👨‍🔬Yitzhak Birk

#### *Abstract*
> Merging two sorted arrays is a prominent building block for sorting and other functions.
Its efficient parallelization requires balancing the load among compute cores, minimizing the
extra work brought about by parallelization, and minimizing inter-thread synchronization
requirements. Efficient use of memory is also important.
>
> We present a novel, visually intuitive approach to partitioning two input sorted arrays
into pairs of contiguous sequences of elements, one from each array, such that 1) each pair
comprises any desired total number of elements, and 2) the elements of each pair form a
contiguous sequence in the output merged sorted array. While the resulting partition and the
computational complexity are similar to those of certain previous algorithms, our approach
is different, extremely intuitive, and offers interesting insights. Based on this, we present a
synchronization-free, cache-efficient merging (and sorting) algorithm.
>
> While we use a shared memory architecture as the basis, our algorithm is easily adaptable
to additional architectures. In fact, our approach is even relevant to cache-efficient sequential
sorting. The algorithms are presented, along with important cache-related insights.
