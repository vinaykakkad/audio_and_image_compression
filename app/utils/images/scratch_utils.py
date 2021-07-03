import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread

from .linalg.svd import svd
from .linalg.utils import rows, cols, mat_splice, mat_multiply, to_int, clip


def image_to_RGBs(image):
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

    return [r, g, b]


def svd_on_RGBs(RGBs, method):
    svd_data = list()
    minimum_rank = None

    for matrix in RGBs:
        start_time = time.time()
        u, s, v_t, rank, iterations = svd(matrix, method)
        duration = start_time - time.time()

        minimum_rank = rank if minimum_rank is None else min(rank, minimum_rank)

        svd_data.append(
            {
                "u": u,
                "s": s,
                "v_t": v_t,
                "rank": rank,
                "iterations": iterations,
                "duration": duration,
            }
        )

    return svd_data, minimum_rank


def reconstruct_RGBs(svd_data, rank):
    reconstruct_data = list()

    for data in svd_data:
        u, s, v_t = data["u"], data["s"], data["v_t"]

        u = mat_splice(u, rows(u), rank)
        s = mat_splice(s, rank, rank)
        v_t = mat_splice(v_t, rank, cols(v_t))

        reconstruct = mat_multiply(mat_multiply(u, s), v_t)
        reconstruct_data.append(reconstruct)
    return reconstruct_data


def RGBs_to_3d_matrix(rows, cols, reconstructed_RGBs):
    final_image = list()
    data_type = "float"

    for row in range(rows):
        current_row = list()

        for col in range(cols):
            pixels = list()

            for matrix in reconstructed_RGBs:
                pixel = matrix[row][col]
                pixels.append(pixel)
                if int(pixel) > 1:
                    data_type = "int"

            current_row.append(pixels)

        final_image.append(current_row)

    return data_type, final_image


def scratch_make_plt_compatible(data_type, matrix):
    if data_type == "int":
        matrix = to_int(matrix)
    else:
        matrix = clip(matrix)

    return matrix


def reconstruct_from_svd(svd_data, rank):
    original_rows = rows(svd_data[0]["u"])
    original_cols = cols(svd_data[0]["v_t"])

    reconstructed_RGBs = reconstruct_RGBs(svd_data, rank)

    data_type, final_image = RGBs_to_3d_matrix(
        original_rows, original_cols, reconstructed_RGBs
    )

    return scratch_make_plt_compatible(data_type, final_image)


def save_scratch_image(path, matrix):
    plt.imshow(matrix)
    plt.axis("off")
    plt.savefig(path)
