from flask import Flask


app = Flask(__name__)


@app.route('/')
def home_page_view():
    return "hello world!!"


if __name__ == "__main__":
    app.run()