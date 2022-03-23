import time

from flask import Flask, abort
import os

app = Flask(__name__)

t = time.time()


@app.route("/")
def hello_world():
    return "<p>Hello, World! " + os.environ['HOSTNAME'] + "</p>"


@app.route("/healthz")
def healthy(name):
    if time.time() - t > 120:
        abort(500, "Oh My God!!!!!")
    return "Ok bro!"


@app.route("/<name>")
def hello(name):
    return f"Hello, {name}!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
