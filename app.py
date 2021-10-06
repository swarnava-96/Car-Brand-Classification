# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 04:04:51 2021

@author: SWARNAVA
"""
# Importing the necessary libraries
from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np

# Keras utils
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

# Defining the flask app
app = Flask(__name__)

# Model
MODEL_PATH = "model_resnet50.h5"

# Loading the trained model
model = load_model(MODEL_PATH)

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size = (224,224))
    
    # Preprocessing the image
    x = image.img_to_array(img)
    
    # Scaling
    x = x/255
    
    # Expanding dimensions
    x = np.expand_dims(x, axis = 0)
    
    # Preprocess
    img_data = preprocess_input(x)
    
    # Prediction
    preds = model.predict(img_data)
    
    # Getting the predicted class
    preds = np.argmax(preds, axis = 1)
    
    # Condition
    if preds == 0:
        preds = "The car is Audi."
    elif preds == 1:
        preds = "The car is Lamborgini."
    else:
        preds = "The car is Mercedes."
        
        
    return preds

@app.route("/", methods = ["GET"])
def index():
    # Main page
    return render_template("index.html")

@app.route("/predict", methods = ["GET", "POST"])
def upload():
    if request.method == "POST":
        # Getting the file from POST request
        f = request.files["file"]
        
        # Saving the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
                basepath, "uploads", secure_filename(f.filename))
        f.save(file_path)
        
        # Make prediction
        preds = model_predict(file_path, model)
        result = preds
        return result
    return None

if __name__ == "__main__":
    app.run(debug = True)
    
    



    
    
    
    
    