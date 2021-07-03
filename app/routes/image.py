from flask import current_app as app
from flask import render_template, redirect, flash
from flask.globals import request
from flask.helpers import url_for

from .utils import numpy_analysis, get_data_from_request
from ..utils.images.main import compress_using_numpy, compress_from_scratch


@app.route("/image/numpy", methods=["POST", "GET"])
def image_numpy_view():
    if request.method == "POST":
        file, file_name, ratio = get_data_from_request(request)

        (
            compressed_file_name, 
            original_shape, 
            lower_rank 
        ) = compress_using_numpy( file, file_name, ratio )

        analysis = numpy_analysis(original_shape, lower_rank)

        context = {
            "compressed_file_name": compressed_file_name,
            "lower_rank": lower_rank, **analysis
        }

        print(context)
        return render_template("image/numpy_results.html", **context)
        
    return render_template("image/numpy.html")


@app.route("/image/scratch", methods=["POST", "GET"])
def image_scratch_view():
    if request.method == "POST":
        file, file_name, ratio = get_data_from_request(request)

        (
            qr_file_name, 
            jacobi_file_name
        ) = compress_from_scratch(file, file_name, ratio)

        context = {
            'qr': qr_file_name,
            'jacobi': jacobi_file_name
        }
        return render_template("image/scratch_results.html", **context)

    return render_template("image/scratch_2.html")