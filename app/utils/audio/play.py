import os

import numpy as np
from scipy.io import wavfile


def audio_play(file, UPLOAD_FOLDER):
	data = np.load(file)

	channels = 1
	try:
		channels = len(data[0])
	except Exception as identifier:
		pass

	data_len = int(len(data) / 2) - 1

	if channels > 1:
		total_length = int(data[0, 0])
		sampling_freq = int(data[1, 0])
		left = data[2:data_len+2, :]
		right = data[-data_len:, :]
	else:
		total_length = int(data[0])
		sampling_freq = int(data[1])
		left = data[2:data_len+2]
		right = data[-data_len:]

	z_len_x = total_length - 2*data_len
	z_len_y = channels
	zeros = np.zeros((z_len_x, z_len_y))

	combine = np.concatenate((left, zeros, right))
	final = np.real(np.fft.ifftn(combine))
	
	filename = f'play_{file.filename[:-4]}.wav'
	wavfile.write(os.path.join(UPLOAD_FOLDER, filename), sampling_freq, 
					final.astype(np.int16))

	return filename