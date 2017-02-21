from flask import render_template, request, json
from io import BytesIO
from PIL import Image, ImageOps
import mxnet as mx
import numpy as np
import os
from collections import namedtuple
from WebApp import app

Batch = namedtuple('Batch', ['data'])

# Load labels
with open('WebApp/synset.txt', 'r') as f:
    synsets = [l.rstrip() for l in f]
# Load model
model = mx.model.FeedForward.load('Model/resnet-152', 0, ctx=mx.cpu())

@app.route("/")
def index():
    return render_template('layout.html')

@app.route("/uploader_ios", methods=['POST'])
def upload_file_ios():

    imagefile = request.files['imagefile']

    img = Image.open(BytesIO(imagefile.read())).convert('RGB')

    # Run some processing and get back image and data
    # I ignore processed image
    _, ret_dta_en = run_some_function_using_image_as_input(img)

    classification = {'English': ret_dta_en}

    return json.dumps(classification)


def run_some_function_using_image_as_input(img):
    img = ImageOps.fit(img, (224, 224), Image.ANTIALIAS)
    # Change shape
    img_np = np.swapaxes(img, 0, 2)
    img_np = np.swapaxes(img_np, 1, 2)
    img_np = img_np[np.newaxis, :]
    # Prediction
    res = model.predict(mx.nd.array(img_np), mx.cpu())
    prob = np.squeeze(res)
    # Category
    a = np.argsort(prob)[-1]
    classification = " ".join(synsets[a].split(" ")[1:]).split(",")[0]
    return img, classification