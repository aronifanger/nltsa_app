from flask import Flask

from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/logistic")
def logistic():
    return render_template('bif.html')

@app.route("/lyap")
def lyap():
    return render_template('lyap.html')

@app.route("/baker")
def baker():
    return render_template('baker.html');

@app.route("/esticadobra")
def esticadobra():
    return render_template("esticadobra.html")


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, use_reloader=True)
