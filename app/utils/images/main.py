from matplotlib.image import imread, imsave
import matplotlib.pyplot as plt
import numpy as np
import time, os

from .utils import to_int
from app.config import COMPRESSED_IMAGE_FOLDER


def decompose(image):
    # Reading the image into a 3-d matrix
    matrix = imread(image)

    # Splitting the r - g - b components
    r = matrix[:, :, 0]
    g = matrix[:, :, 1]
    b = matrix[:, :, 2]

    # Converting the ndarrays to python list
    r = np.ndarray.tolist(r)
    g = np.ndarray.tolist(g)
    b = np.ndarray.tolist(b)

    return r, g, b


def numpy_compression(image, file_name, ratio):
    # original matrix has the shape(x, y, 3)
    matrix = imread(image)
    original_shape = matrix.shape[:2]

    # transforming to shape (3, x, y)
    matrix_transformed = np.transpose(matrix, (2, 0, 1))

    # applying svd
    u, s, v_t = np.linalg.svd(matrix_transformed)
    rank = s.shape[1]

    # converting 1d s returned from svd to diagonal matrix
    sigma = np.zeros((3, matrix.shape[0], matrix.shape[1]))
    for j in range(3):
        np.fill_diagonal(sigma[j, :, :], s[j, :])

    # low rank approximation
    lower_rank = int(ratio * rank / 100)
    compressed_img = u @ sigma[..., :lower_rank] @ v_t[..., :lower_rank, :]

    # transforming back to get the shape ( x, y, 3)
    transformed_img = np.transpose(compressed_img, (1, 2, 0))

    # if the values are > 1, converting all the values to int
    # if values are near the range(0, 1), clippint them to 0-1
    max_value = np.max(transformed_img)

    if max_value > 1.5:
        transformed_img = transformed_img.astype(np.uint8)
    else:
        transformed_img = np.clip(transformed_img, a_max=1.0, a_min=0.0)

    # Ensuring a unique file name for every file
    counter = 0
    while os.path.exists(
        os.path.join(COMPRESSED_IMAGE_FOLDER, f"{counter}_{file_name}")
    ):
        counter += 1

    path = os.path.join(COMPRESSED_IMAGE_FOLDER, f"{counter}_{file_name}")
    imsave(path, transformed_img)

    return f"{counter}_{file_name}", original_shape, lower_rank
