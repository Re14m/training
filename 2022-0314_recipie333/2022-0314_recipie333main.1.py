#!/usr/bin/env python
# coding: utf-8

from flask import Flask, jsonify
from flask_cors import CORS
from api.get_texts import api

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CORS(app)
app.register_blueprint(api, url_prefix="/api")

data = {"message":"こんにちは"}

@app.route("/")
def hello_world():
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
