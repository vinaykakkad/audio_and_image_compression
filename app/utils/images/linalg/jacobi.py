import math

from .utils import (
    eye,
    rows,
    cols,
    transpose,
    mat_multiply,
)


def jacobi(size, row, col, theta):
    """
    Fuction to construct jacobi rotation matrix
    """

    mat = eye(size)

    mat[row][row] = mat[col][col] = math.cos(theta)
    mat[row][col] = -1 * math.sin(theta)
    mat[col][row] = math.sin(theta)

    return mat


def max_off_diag(matrix):
    """
    Funciton which return the maximum off-diagonal element, its indices and
    the angle for the corresponding jacobi rotation matrix
    """

    max_n = abs(matrix[0][1])
    r, c = 0, 1

    # Finding the maximum element and its indices
    for row in range(rows(matrix)):
        for col in range(cols(matrix)):
            if row != col and abs(matrix[row][col]) > max_n:
                max_n = abs(matrix[row][col])
                r, c = row, col

    if max_n == 0:
        return (0, 0, 0, 0)
    else:
        mat_r_c = matrix[r][c]
        mat_r_r = matrix[r][r]
        mat_c_c = matrix[c][c]

        if mat_c_c == mat_r_r:
            theta = math.pi / 2
        else:
            theta = math.atan(2 * mat_r_c / (mat_r_r - mat_c_c))

        return (max_n, r, c, theta / 2)


def eig(matrix):
    """
    Main funciton to find the eigenvalues and eigenvectors of a symmetric
    matrix using jacobi eigenvalue algorithm
    """

    size = cols(matrix)

    max_n, r, c, theta = max_off_diag(matrix)
    eig_vector = eye(size)
    eig_value = matrix

    counter = 0
    while max_n > math.exp(-8):
        rot_jacobi = jacobi(size, r, c, theta)
        eig_value = mat_multiply(transpose(rot_jacobi), eig_value)
        eig_value = mat_multiply(eig_value, rot_jacobi)
        eig_vector = mat_multiply(eig_vector, rot_jacobi)

        counter += 1
        max_n, r, c, theta = max_off_diag(eig_value)

    return (eig_vector, eig_value, counter)
