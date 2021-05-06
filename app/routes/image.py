from flask import current_app as app


@app.route('/image/numpy', methods=['POST', 'GET'])
def image_numpy_view():
	return "hello"


@app.route('/image/naive', methods=['POST', 'GET'])
def image_naive_view():
	return "hello"