import os

import numpy as np
from scipy.io import wavfile
import plotly.graph_objects as go
import plotly.io as pio

from .play import audio_play
from ...config import COMPRESS_FOLDER


def create_plot(data, channels, x_label, y_label, title):
    """Function to create html string for interactive visualisations

    Args:
            data (n-d array): N-D array containg the audio data
            channels (int): no. of channels in the audio data
            x_label (str): x-axis label
            y_label (str): y-axis label
            title (str): title of graph

    Returns:
            str: html string for visualisation
    """

    # customising the layout of the graph
    layout = go.Layout(
        title=title,
        xaxis=dict(
            title=x_label, tickcolor="#666666", gridcolor="#666666", gridwidth=0.5
        ),
        yaxis=dict(
            title=y_label, tickcolor="#666666", gridcolor="#666666", gridwidth=0.5
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        colorway=["white", "rgb(46, 255, 123)"],
    )
    fig = go.Figure(layout=layout)

    # creating the graph
    if channels == 1:
        curr_channel = data.tolist()
        fig.add_trace(go.Scatter(y=curr_channel, name="channel_1"))
    else:
        for i in range(channels):
            curr_channel = np.real((data[:, i])).tolist()
            fig.add_trace(go.Scatter(y=curr_channel, name=f"channel_{i}"))

    html_str = pio.to_html(fig, include_plotlyjs=False, full_html=False)

    return html_str


def audio_compress(file, file_name, compression_ratio):
    """Function to perform the compression and create visualisations

    Args:
            file (str / file): path to file / audio file
            file_name (str)
            compression_ratio (int)

    Returns:
            compressed_data_file (str): name of compressed_data_file
                        compressed_audio_file (str): name of compressed audio file
                        data_plot (str): html string for original data
                        fft_plot (str): html string for fft data
    """

    # defining the parameters
    preserve_ratio = compression_ratio / 1600
    sampling_freq, data = wavfile.read(file)

    channels = 1
    try:
        channels = len(data[0])
    except Exception as identifier:
        pass

    # applying FFT
    fft_data = np.fft.fftn(data)

    # creating the visualisations
    data_plot = create_plot(data, channels, "Data_points", "Values", "Original Data")
    fft_plot = create_plot(
        np.real(fft_data), channels, "Data_points", "Values", "After applying FFT"
    )

    # removing the less significat part from center for compression
    preserve_length = int(preserve_ratio * len(data))
    data_to_pad = np.empty((2, channels))

    if channels > 1:
        trucated_l = fft_data[:preserve_length, :]
        trucated_r = fft_data[-preserve_length:, :]
        data_to_pad[0, 0] = len(data)
        data_to_pad[1, 0] = sampling_freq
    else:
        trucated_l = fft_data[:preserve_length]
        trucated_r = fft_data[-preserve_length:]
        data_to_pad = np.empty((2,))
        data_to_pad[0] = len(data)
        data_to_pad[1] = sampling_freq

    # combining and saving the compressed data
    combined = np.concatenate((data_to_pad, trucated_l, trucated_r))

    compressed_data_file = f"compressed_{file_name[:-4]}"
    np.save(os.path.join(COMPRESS_FOLDER, compressed_data_file), combined)
    compressed_data_file = f"{compressed_data_file}.npy"

    # getting the compressed audio file
    compressed_audio_file = audio_play(
        os.path.join(COMPRESS_FOLDER, compressed_data_file), compressed_data_file
    )

    return compressed_data_file, compressed_audio_file, data_plot, fft_plot
