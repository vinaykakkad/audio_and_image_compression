import numpy as np
from matplotlib.image import imsave

from .numpy_utils import (
    get_unique_path,
    image_to_matrix,
    list_to_diag_matrix,
    np_reconstruct_from_svd,
    np_make_matplotlib_compilant,
)
from .scratch_utils import (
    svd_on_RGBs,
    image_to_RGBs,
    save_scratch_image,
    reconstruct_from_svd
)


def compress_from_scratch(image, file_name, ratio):
    RGBs = image_to_RGBs(image)

    qr_svd_data, qr_rank = svd_on_RGBs(RGBs, 'qr')
    jacobi_svd_data, jacobi_rank = svd_on_RGBs(RGBs, 'jacobi')

    final_qr = reconstruct_from_svd(qr_svd_data, int(ratio * qr_rank / 100))
    final_jacobi = reconstruct_from_svd(
        jacobi_svd_data, int(ratio * jacobi_rank / 100)
    )

    path, qr_counter = get_unique_path(f"qr_{file_name}")
    save_scratch_image(path, final_qr)
    path, jacobi_counter = get_unique_path(f"jacobi_{file_name}")
    save_scratch_image(path, final_jacobi)

    qr_file_name = f"{qr_counter}_qr_{file_name}"
    jacobi_file_name = f"{jacobi_counter}_jacobi_{file_name}"

    return (qr_file_name, jacobi_file_name)


def compress_using_numpy(image, file_name, ratio):
    matrix, original_shape = image_to_matrix(image)

    u, s, v_t = np.linalg.svd(matrix)
    rank = s.shape[1]

    sigma = list_to_diag_matrix(matrix.shape, s)

    compressed_matrix, lower_rank = np_reconstruct_from_svd(
        ratio, rank, u, sigma, v_t
    )

    compressed_matrix = np_make_matplotlib_compilant(compressed_matrix)

    path, counter = get_unique_path(file_name)
    imsave(path, compressed_matrix)

    return f"{counter}_{file_name}", original_shape, lower_rank