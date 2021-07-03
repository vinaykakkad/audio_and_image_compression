import math


def print_matrix(matrix):
    """
    Function to print a matrix
    """

    for row in matrix:
        for col in row:
            print("%.3f" % col, end=" ")
        print()


def rows(matrix):
    """
    Returns the no. of rows of a matrix
    """

    if type(matrix) != list:
        return 1
    return len(matrix)


def cols(matrix):
    """
    Returns the no. of columns of a matrix
    """

    if type(matrix[0]) != list:
        return 1
    return len(matrix[0])


def eye(size):
    """
    Returns an identity matrix
    """

    mat = list()
    for r in range(size):
        row = list()
        for c in range(size):
            if r == c:
                row.append(1)
            else:
                row.append(0)
        mat.append(row)

    return mat


def pivot_index(row):
    """
    Returns the index of pivot in a row
    """

    counter = 0

    for element in row:
        if element != float(0):
            return counter
        counter += 1

    return counter


def pivot_value(row):
    """
    Returns the value of pivot in a row
    """

    for element in row:
        if element > math.exp(-8):
            return element

    return 0


def swap(matrix, index_1, index_2):
    """
    Function to swap two rows
    """

    x = matrix[index_1]
    matrix[index_1] = matrix[index_2]
    matrix[index_2] = x


def transpose(matrix):
    """
    Returns the transpose of a matrix
    """

    transpose_matrix = list()

    for i in range(cols(matrix)):
        row = list()

        for j in range(rows(matrix)):
            row.append(matrix[j][i])

        transpose_matrix.append(row)

    return transpose_matrix


def mat_multiply(a, b):
    """
    Function to multiply two matrices
    """

    c = [[0 for i in range(cols(b))] for j in range(rows(a))]

    for i in range(rows(a)):
        for j in range(cols(b)):
            for k in range(rows(b)):
                c[i][j] += a[i][k] * b[k][j]
    return c


def mat_splice(matrix, r, c):
    """
    Function which returns a matrix with the first r rows and first c
    columns of the original matrix
    """

    result = list()

    for i in range(r):
        row = matrix[i]
        result.append(row[:c])

    return result


def to_int(matrix):
    """
    Funciton to convert the eact element of the matrix to int
    """

    for row in range(rows(matrix)):
        for col in range(cols(matrix)):
            for j in range(3):
                matrix[row][col][j] = int(matrix[row][col][j])

    return matrix


def clip(matrix):
    """
    Function to clip each element to the range float[0, 1]
    """

    for row in range(rows(matrix)):
        for col in range(cols(matrix)):
            for j in range(3):
                if matrix[row][col][j] > 1:
                    matrix[row][col][j] = 1
                if matrix[row][col][j] < 0:
                    matrix[row][col][j] = 0

    return matrix
