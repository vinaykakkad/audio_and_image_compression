import math, copy

from .utils import (
    eye,
    rows,
    cols,
    transpose,
    mat_multiply,
)


def is_diagonal(matrix):
    """
    Funciton to check if the matrix is diagonal
    """
    for r in range(rows(matrix)):
        for c in range(cols(matrix)):
            if r != c:
                if abs(matrix[r][c]) > math.exp(-8):
                    return False
    return True


def qr(matrix):
    """
    Funciton whic returns the qr - decomposition of a matrix
    """

    original = copy.deepcopy(matrix)
    Q = list()

    counter = 0
    for i in range(cols(matrix)):
        u = list()
        u.append(matrix[i])

        # Making the orthogonal basis by grahm schmidt
        for j in range(0, counter):
            v_i = list()
            v_i.append(Q[j])
            v_i_transpose = transpose(v_i)
            v_dot_u = mat_multiply(u, v_i_transpose)
            for i in range(cols(u)):
                u[0][i] = u[0][i] - v_i[0][i] * float(v_dot_u[0][0])

        normalised_u = list()
        u_dot_u = mat_multiply(u, transpose(u))
        for x in u[0]:
            if float(u_dot_u[0][0]) < math.exp(-8):
                x = 0
            else:
                x = x / math.sqrt(float(u_dot_u[0][0]))
            normalised_u.append(x)

        Q.append(normalised_u)
        counter += 1

    # Finding R by multiplying Q-Transpose With original matrix
    R = mat_multiply(Q, original)
    Q = transpose(Q)

    return (Q, R)


def qr_eig(matrix):
    """
    Funciton which finds the eigenvalues and eigenvectors of a matrix
    using QR decomposition
    """

    counter = 0
    eig_vectors = eye(cols(matrix))

    while not is_diagonal(matrix):
        q, r = qr(matrix)
        eig_vectors = mat_multiply(eig_vectors, q)
        matrix = mat_multiply(r, q)
        counter += 1

    return (eig_vectors, matrix, counter)
