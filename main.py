from flask import Flask

from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/bif")
def index():
    return render_template('bif.html')


@app.route("/baker")
def baker():
    return render_template('baker.html');


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, use_reloader=True)
