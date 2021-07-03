import os

from ..config import SAMPLE_IMAGE_FOLDER


def get_data_from_request(request):
    data_from = request.form["from"]
    ratio = int(request.form["ratio"])

    # defining the file and filename
    if data_from == "sample":
        file_name = request.form["file_name"]
        file = os.path.join(SAMPLE_IMAGE_FOLDER, file_name)
    else:
        file = request.files.get("file")
        file_name = file.filename

    return file, file_name, ratio


def numpy_analysis(original_shape, lower_rank):
    original_width = original_shape[0]
    original_height = original_shape[1]
    
    original_data_points = original_height * original_width
    compressed_data_points = original_width * lower_rank \
                                + lower_rank * lower_rank \
                                + lower_rank * original_height

    percentage = round(compressed_data_points / original_data_points, 2)

    return {
        'o_height': original_height,
        'o_width': original_width,
        'o_data_points': original_data_points,
        'c_data_points': compressed_data_points,
        'percentage': percentage
    }
