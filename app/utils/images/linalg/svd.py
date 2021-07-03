import math
from operator import itemgetter

first_item = itemgetter(0)

from .qr import qr_eig
from .jacobi import eig
from .utils import (
    eye,
    rows,
    mat_multiply,
    transpose,
)


def svd(matrix, approach):
    """
    Funciton to perform svd on a matrix
    """

    # Getting the eigenvalues and vectors of transpose(A) * A for V and Sigma
    a = mat_multiply(transpose(matrix), matrix)
    if approach == "qr":
        V, sigma, iterations = qr_eig(a)
    else:
        V, sigma, iterations = eig(a)

    # Sorting singular values and the colums of V accordingly
    V = transpose(V)

    singular_values = list()
    sorted_V = list()

    r = 0
    for i in range(rows(sigma)):
        singular_values.append([(sigma[i][i]), i])
        if sigma[i][i] > math.exp(-8):
            r += 1

    singular_values.sort(key=first_item, reverse=True)

    sigma_r = eye(r)
    sigma_r_inv = eye(r)

    # Constructing the sorted U and sigma matrices
    i, j = 0, 0
    for value in singular_values:
        if value[0] > math.exp(-8):
            sorted_V.append(V[value[1]])
            sigma_r[j][j] = value[0] ** (1 / 2)
            sigma_r_inv[j][j] = 1 / (value[0] ** (1 / 2))
            j += 1
        i += 1

    # Constructing U by multiplying V and sigma inverse
    sorted_U = mat_multiply(mat_multiply(matrix, transpose(sorted_V)), sigma_r_inv)

    return (sorted_U, sigma_r, sorted_V, r, iterations)
