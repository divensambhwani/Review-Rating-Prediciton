#!/usr/bin/env python
# coding: utf-8

#!pip install http://download.pytorch.org/whl/cpu/torch-1.0.0-cp36-cp36m-linux_x86_64.whl
#!pip install fastai
#!pip install HealthCheck
#!pip install google-cloud-storage
#!pip install google-cloud-logging



from fastai.text import *
from flask import Flask, jsonify, request
from healthcheck import HealthCheck


import logging

import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()

app = Flask(__name__)
path = Path('')
learn = load_learner(path)

#For flask
#logging.basicConfig(filename="flask.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.info("Model and vocab loaded")
print("Model Loaded")


health = HealthCheck(app, "/hcheck")

def healthcheck_func():
    return True, "Everything is up and running"

health.add_check(healthcheck_func)


def predict_func(text):
  result = learn.predict(text)
  return result


@app.route('/seclassifier', methods=['POST'])
def predict_sentiment():
    text = request.get_json()['text']
    #print(text)
    predictions = predict_func(text)
    predictions=str(predictions[0])
    #print(predictions)
    app.logger.info("Text:" + text +"Prediction:" + predictions)
    return jsonify({'Text': text,'predictions':predictions})



if __name__ == "__main__":
  app.run(host='0.0.0.0', port='8000')


