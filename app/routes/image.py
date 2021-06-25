import os

from flask import current_app as app
from flask import render_template, redirect, flash
from flask.globals import request
from flask.helpers import url_for

from ..config import SAMPLE_IMAGE_FOLDER
from ..utils.images.main import numpy_compression


@app.route("/image/numpy", methods=["POST", "GET"])
def image_numpy_view():
    if request.method == "POST":
        data_from = request.form["from"]
        ratio = int(request.form["ratio"])

        # defining the file and filename
        if data_from == "sample":
            file_name = request.form["file_name"]
            file = os.path.join(SAMPLE_IMAGE_FOLDER, file_name)
        else:
            file = request.files.get("file")
            file_name = file.filename

        (compressed_file_name, original_shape, lower_rank) = numpy_compression(
            file, file_name, ratio
        )

        original_data_points = original_shape[0] * original_shape[1]

        compressed_data_points = (
            original_shape[0] * lower_rank + lower_rank + lower_rank * original_shape[1]
        )

        context = {
            "compressed_file_name": compressed_file_name,
            "original_width": original_shape[0],
            "original_height": original_shape[1],
            "original_data_points": original_data_points,
            "lower_rank": lower_rank,
            "compressed_data_points": compressed_data_points,
            "percentage": round(compressed_data_points / original_data_points, 2),
        }

        return render_template("image/numpy_results.html", **context)
    return render_template("image/numpy.html")


@app.route("/image/scratch", methods=["POST", "GET"])
def image_scratch_view():
    if request.method == "POST":
        data_from = request.form["from"]

        # defining the file and filename
        if data_from == "sample":
            file_name = request.form["file_name"]
            file = os.path.join(SAMPLE_IMAGE_FOLDER, file_name)
        else:
            file = request.files.get("file")
            file_name = file.filename
            temp = file.read()

            if not file.filename.endswith(".png"):
                flash("Only png files are accepted", "error")
                return redirect(url_for("image_scratch_view"))

            if len(temp) > 800:
                flash("File is too large", "error")
                return redirect(url_for("image_scratch_view"))

    return render_template("image/scratch.html")
