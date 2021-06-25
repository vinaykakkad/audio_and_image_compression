import os

from flask import current_app as app
from flask import render_template, redirect, request, flash, Response
from flask.helpers import url_for

from ..utils.audio.compress import audio_compress
from ..utils.audio.play import audio_play
from ..config import SAMPLE_AUDIO_FOLDER


@app.route("/audio/compress", methods=["POST", "GET"])
def audio_compress_view():
    """View for audio compression

    GET: Renders the template

    POST: Returns
            - html string for original data
            - html string for fft data
            - name of compressed data file
            - name of compressed audion file
    """
    if request.method == "POST":
        data_from = request.form["from"]

        # defining the file and filename
        if data_from == "sample":
            file_name = request.form["file_name"]
            file = os.path.join(SAMPLE_AUDIO_FOLDER, file_name)
        else:
            file = request.files.get("file")
            file_name = file.filename

            if not file.filename.endswith(".wav"):
                flash("Only wav files are accepted", "error")
                return redirect(url_for("audio_compress_view"))

        (
            compressed_data_file,
            compressed_audio_file,
            data_plot,
            fft_plot,
        ) = audio_compress(file, file_name, 80)

        context = {
            "data_file_url": compressed_data_file,
            "audio_file_url": compressed_audio_file,
            "original_plot": data_plot,
            "fft_plot": fft_plot,
        }
        return render_template("audio/results.html", **(context))

    return render_template("audio/compress.html")


@app.route("/audio/play", methods=["POST", "GET"])
def audio_play_view():
    if request.method == "POST":
        file = request.files.get("file")

        if not file.filename.endswith(".npy"):
            flash("Only .npy will files are accepted", "error")
            return redirect(url_for("audio_play_view"))
        else:
            filename = audio_play(file, file.filename)

            context = {"file": filename}
            return render_template("audio/play.html", **(context))
    return render_template("audio/play.html")
