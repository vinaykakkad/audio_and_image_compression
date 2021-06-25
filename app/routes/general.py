from flask import current_app as app
from flask import render_template


@app.route("/")
def home_page_view():
    return render_template("home/home.html")
