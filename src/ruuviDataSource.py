from flask import Flask, render_template, jsonify, request
from util.grafana import *
from util.ruuvi import start_ruuvi_workers
import datetime as dt
import json
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('conf.py')

# Logging
formatter = logging.Formatter("[%(asctime)s] [%(pathname)s:%(lineno)d] %(levelname)s - %(message)s")
if app.config['LOG_FILE']:
    handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10000000, backupCount=5)
else:
    handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger = logging.getLogger('ruuvipi')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


# Start worker threads
start_ruuvi_workers(app.config['TAGS'], app.config['DATA_FETCH_DELAY'], app.config['DATABASE'])


@app.route("/")
def grafana_index():
    """
    Required by JSON plugin
    """
    logger.info("{} {}".format(request.method, request.path))
    return "OK"

@app.route("/search", methods=["POST"])
def grafana_search():
    logger.info("{} {}".format(request.method, request.path))
    return jsonify(app.config['TAGS'])

@app.route("/query", methods=["POST"])
def grafana_query():
    logger.info("{} {}".format(request.method, request.path))
    try:
        response = prepare_grafana_query_data(request.json)
        return jsonify(response)
    except Exception as e:
        logger.error(e)
        return jsonify({"error": "unknown error occured"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
