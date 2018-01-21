# cython: profile=True
import cython

import numpy as np
cimport numpy as np

from scipy.spatial.distance import squareform

DTYPE = np.float
DTYPEint = np.int

ctypedef np.float_t DTYPE_t
ctypedef np.int_t DTYPEint_t

@cython.profile(False)
cdef unsigned int countlower(np.ndarray[DTYPE_t, ndim=1] vec1,
                             np.ndarray[DTYPE_t, ndim=1] vec2,
                             int n1, int n2):
    # Function output corresponds to np.bincount(v1 < v2)[1]

    assert vec1.dtype == DTYPE and vec2.dtype == DTYPE

    cdef unsigned int i, j
    cdef unsigned int trues = 0
    cdef unsigned int* pointer1 = <unsigned int*> vec1.data
    cdef unsigned int* pointer2 = <unsigned int*> vec2.data

    for i in range(n1):
        for j in range(n2):
            if pointer1[i] < pointer2[j]:
                trues += 1

    return trues


def gamma(np.ndarray[DTYPE_t, ndim=2] Y, np.ndarray[DTYPEint_t, ndim=1] part):
    assert Y.dtype == DTYPE and part.dtype == DTYPEint

    if len(Y) != len(part):
        raise ValueError('Distance matrix and partition must have same shape')

    # defined locals
    cdef unsigned int K, c_label, n_, trues
    cdef unsigned int s_plus = 0
    cdef unsigned int s_minus = 0

    # assigned locals
    cdef np.ndarray n_in_ci = np.bincount(part)
    cdef int num_clust = len(n_in_ci) - 1
    cdef np.ndarray s = np.zeros(len(Y), dtype=DTYPE)

    # Partition should have at least two clusters
    K = len(set(part))
    if K < 2:
        return 0
    # Loop through clusters
    for c_label in range(1, K+1):
        dist_within = squareform(Y[part == c_label][:, part == c_label])
        dist_between = np.ravel(Y[part == c_label][:, part != c_label])
        n1 = len(dist_within)
        n2 = len(dist_between)

        trues = countlower(dist_within, dist_between, n1, n2)
        s_plus += trues
        s_minus += n1 * n2 - trues

    n_ =  s_plus + s_minus

    return (<double>s_plus - <double>s_minus) / <double>n_ if n_ != 0 else 0