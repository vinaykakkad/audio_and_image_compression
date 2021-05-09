import os

import numpy as np
from scipy.io import wavfile

from ...config import PLAY_FOLDER


def audio_play(file, file_name):
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
	
	if channels > 1:
		zeros = np.zeros((z_len_x, channels))
	else:
		zeros = np.zeros((z_len_x,))
		

	combine = np.concatenate((left, zeros, right))
	final = np.real(np.fft.ifftn(combine))
	
	filename = f'play_{file_name[:-4]}.wav'
	wavfile.write(os.path.join(PLAY_FOLDER, filename), sampling_freq, 
					final.astype(np.int16))

	return filename