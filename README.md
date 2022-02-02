
# Audio and Image compression 🗜

The projects includes implementation of [Jacobi Eigenvalue Theorem](https://en.wikipedia.org/wiki/Jacobi_eigenvalue_algorithm#:~:text=In%20numerical%20linear%20algebra%2C%20the,a%20process%20known%20as%20diagonalization), [QR Algorithm](https://en.wikipedia.org/wiki/QR_algorithm), [Singular Value Decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition) and [Fast Fourier Transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform) to perform lossy image and audio compression.

Jacobi Eigenvalue Algorithm, QR Algorithm and Singular Value Decomposition have been implemented from scratch to get a better understanding on the working of such algorithms.

A web interface has been made to make the project more accessible to others.

*Some part of the project is not on the web interface due to the heroku free dyno. The complete script is on other brnach*

## Demo 💻

[Demo](https://vk-compression.herokuapp.com/)

  
## Environment Variables ⚙

To run this project, you will need to add the following environment variables to a .env file

`SECRETY_KEY` - Secret key for the flask app

  
## Run Locally 🚀

Clone the project
```bash
  git clone https://github.com/vinaykakkad/audio_and_image_compression.git
```

Creatre a virtual environment and activate
```bash
  python -m venv env

  env\Scripts\activate
```

Install dependencies
```bash
  pip install -r requirements.txt
```

Run locally using
```bash

  python app.py
```

  
## Tech Stack 👨‍💻

**Backend:** Flask, numpy, scipy, matplotlib, plotly

**Frontend:** HTML, CSS, Bootstrap5

  
## License 🔐

[MIT](https://github.com/vinaykakkad/audio_and_image_compression/blob/main/LICENSE)

  
