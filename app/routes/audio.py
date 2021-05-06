import os

from flask import current_app as app
from flask import render_template, redirect, request, flash

from ..utils.audio.compress import audio_compress
from ..utils.audio.play import audio_play


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAY_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'play')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'compress')


@app.route('/audio/compress', methods=['POST', 'GET'])
def audio_compress_view():
	if request.method == 'POST':
		file = request.files.get('file')

		if not file.filename.endswith('.wav'):
			flash('Only wav files are accepted', 'error')
			return redirect('/audio/compress')
		else:
			filename, original_plot, fft_plot = audio_compress(file, 80, UPLOAD_FOLDER)

			context = {'file': filename, 'original_plot': original_plot,
					'fft_plot': fft_plot}
			return render_template('audio/results.html', **(context))
	return render_template('audio/compress.html')


@app.route('/audio/play', methods=['POST', 'GET'])
def audio_play_view():
	if request.method == 'POST':
		file = request.files.get('file')

		if not file.filename.endswith('.npy'):
			flash('Only .npy will files are accepted', 'error')
			return redirect('/audio/play')
		else:
			filename = audio_play(file, PLAY_FOLDER)

			context = { 'file': filename }
			return render_template('audio/play.html', **(context))
	return render_template('audio/play.html')