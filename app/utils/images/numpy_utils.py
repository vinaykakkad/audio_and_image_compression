import os

import numpy as np
from matplotlib.image import imread

from app.config import COMPRESSED_IMAGE_FOLDER


def image_to_matrix(image):
    """original matrix has the shape(x, y, 3)
    transforming to shape (3, x, y)"""
    matrix = imread(image)
    matrix_transformed = np.transpose(matrix, (2, 0, 1))

    return matrix_transformed, matrix.shape


def list_to_diag_matrix(shape, s):
    """convert 1d(s) to diagonal matrix(sigma)"""
    sigma = np.zeros((3, shape[1], shape[2]))
    for j in range(3):
        np.fill_diagonal(sigma[j, :, :], s[j, :])
    return sigma


def np_reconstruct_from_svd(ratio, rank, u, sigma, v_t):
    """low rank approximation and rearrangement"""
    # low rank approximation
    lower_rank = int(ratio * rank / 100)
    compressed_matrix = u @ sigma[..., :lower_rank] @ v_t[..., :lower_rank, :]

    # transforming back to get the shape ( x, y, 3)
    compressed_matrix = np.transpose(compressed_matrix, (1, 2, 0))
    return compressed_matrix, lower_rank


def np_make_matplotlib_compilant(matrix):
    """For image to show in matplotlib:
    - If values are floats near the range[0, 1]:
        No values should exceed [0, 1]
    - If values are in the range [0, 255]
        No values should be a floast"""
    max_value = np.max(matrix)

    if max_value > 1.5:
        matrix = matrix.astype(np.uint8)
    else:
        matrix = np.clip(matrix, a_max=1.0, a_min=0.0)

    return matrix


def get_unique_path(file_name):
    """Save file while ensuring a unique file_name"""
    counter = 0
    while os.path.exists(
        os.path.join(COMPRESSED_IMAGE_FOLDER, f"{counter}_{file_name}")
    ):
        counter += 1

    path = os.path.join(COMPRESSED_IMAGE_FOLDER, f"{counter}_{file_name}")

    return path, counter
