import os

import numpy as np
from scipy.io import wavfile
import plotly.graph_objects as go
import plotly.io as pio


def create_plot(data, channels, x_label, y_label, title):
	layout = go.Layout(
		title=title,
		xaxis=dict(title=x_label, tickcolor='#666666', gridcolor='#666666',
				gridwidth=0.5),
		yaxis=dict(title=y_label, tickcolor='#666666', gridcolor='#666666',
				gridwidth=0.5), 
		paper_bgcolor='rgba(0,0,0,0)',
		plot_bgcolor='rgba(0,0,0,0)',
		font_color='white',
		colorway=['white', 'rgb(46, 255, 123)'] 
	) 
	fig = go.Figure(layout=layout)

	if channels == 1:
		curr_channel = data.tolist()
		fig.add_trace(go.Scatter(y=curr_channel, name='channel_1'))
	else:
		for i in range(channels):
			curr_channel = np.real((data[:, i])).tolist()
			fig.add_trace(go.Scatter(y=curr_channel, name=f'channel_{i}'))

	html_str = pio.to_html(fig, include_plotlyjs=False, full_html=False)
	
	return html_str


def audio_compress(file, compression_ratio, UPLOAD_FOLDER):
	preserve_ratio = compression_ratio / 1600

	sampling_freq, data = wavfile.read(file)
	fft_data = np.fft.fftn(data)
	
	channels = 1
	try:
		channels = len(data[0])
	except Exception as identifier:
		pass

	data_plot = create_plot(data, channels, 'Data_points', 
							'Values', 'Original Data')
	fft_plot = create_plot(fft_data, channels, 'Data_points', 
							'Values', 'After applying FFT')

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
		data_to_pad[0] = len(data)
		data_to_pad[1] = sampling_freq
		
	combined = np.concatenate((data_to_pad, trucated_l, trucated_r))

	filename = f'compressed_{file.filename[:-4]}'
	np.save(os.path.join(UPLOAD_FOLDER, filename), combined)

	return filename, data_plot, fft_plot