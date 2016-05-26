"""some stuff.

that says some things
"""
from __future__ import division
# from matplotlib import pyplot as plt
import math

def vector_add(x, y):
    """add vector."""
    return [v_i+w_i for v_i, w_i in zip(x, y)]


def vector_subtract(x, y):
    """subtract vector."""
    return [v_i - w_i for v_i, w_i in zip(x, y)]


def vector_sum(vectors):
    """sum all elements in vector."""
    return reduce(vector_add, vectors)


def scalar_multiply(c, v):
    """c is a number, v a vector."""
    return [c * v_i for v_i in v]


def vector_mean(vectors):
    """compute vector mean of vectors."""
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))


def dot_product(v, w):
    """compute dot product."""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


def sum_of_squares(v):
    """compute v_1^2 + v_2^2..."""
    return dot_product(v, v)


def magnitude(v):
    """compute magnitude."""
    return math.sqrt(sum_of_squares(v))


def squared_distance(v, w):
    """compute squared distance."""
    return sum_of_squares(vector_subtract(v, w))


def distance(v, w):
    """compute distance."""
    return magnitude(vector_subtract(v, w))

# MATRIX OPERATIONS


def shape(A):
    """return shape."""
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return num_rows, num_cols


def get_row(A, i):
    """return row i from A."""
    return A[i]


def get_column(A, j):
    """return col j from A."""
    return [A_i[j] for A_i in A]


def make_matrix(num_rows, num_cols, entry_fn):
    """make a matrix."""
    return [[entry_fn(i, j) for j in range(num_cols)] for i in range(num_cols)]


def is_diagonal(i,j):
    """1's on the diagonal, 0's elsewhere"""
    return 1 if i == j else 0

# DATA DESCRIPTION


def mean(x):
    return sum(x)/len(x)


def median(v):
    """finds the middle-most value of v"""
    n = len(v)
    sorted_v = sorted(v)
    midpoint = n // 2

    if (n % 2) == 1:
        #if odd, return the middle value
        return sorted_v[midpoint]
    else:
        lo = midpoint - 1
        hi = midpoint
        return (sorted_v[lo] + sorted_v[hi]) / 2


def quantile(x, p):
    """ returns the p-th percentile of x"""
    p_index = int(p * len(x))
    return sorted(x)[p_index]


def mode(x):
    """returns most common value"""
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.iteritems()
            if count == max_count]


def data_range(x):
    return max(x) - min(x)


def de_mean(x):
    """translate by subtracting mean"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]


def variance(x):
    """assumes x has at least 2 elements"""
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)


def standard_deviation(x):
    return math.sqrt(variance(x))


def covariance(x,y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n-1)

def correlation(x,y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x,y) / stdev_x / stdev_y
    else:
        return 0


# stats / random deviations

def uniform_pdf(x):
    return 1 if x >= 0 and x < 1 else 0


def normal_pdf(x, mu=0, sigma=1):
    sqrt_two_pi = math.sqrt(2 * math.pi)
    return (math.exp(-(x-mu) ** 2 / 2 / sigma ** 2) / (sqrt_two_pi * sigma))


def bernoulli_trial(p):
    return 1 if random.random() < p else 0

def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n)) 
