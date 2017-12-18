import os
import time

from flask import Flask, render_template, request
from werkzeug import secure_filename
import tensorflow as tf
import cv2
import numpy as np

from utils import detect_faces, compile_models, check_ak_or_namo

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

model_ak, model_nm, graph = compile_models()
haar_face_cascade = cv2.CascadeClassifier(os.path.join(APP_ROOT,'models/data/haarcascade_frontalface_alt.xml'))

@app.route("/")
def index():
	return render_template("upload.html")

@app.route("/", methods=['POST'])
def upload():
	target = os.path.join(APP_ROOT, 'static/images/')
	print ("TARGET: ", target)

	if not os.path.isdir(target):
		os.mkdir(target)

	file = request.files['file']
	print ("File: ", file)
	filename = file.filename
	destination = os.path.join(APP_ROOT, 'static/images/')+str(secure_filename(file.filename))
	file.save(destination)
	print ("Location:" + destination)
	img = cv2.imread(os.path.join(APP_ROOT, destination))
	n_faces, faces_detected_img = detect_faces(haar_face_cascade, img)
	faces="No"
	AK="No"
	NM="No"
	if n_faces > 0:
            faces = "Yes"
            with graph.as_default():
                if (check_ak_or_namo(destination, model_ak) == True):
                    AK = "Yes"
                if (check_ak_or_namo(destination, model_nm) == True):
                    NM = "Yes"
	cv2.imwrite(destination, faces_detected_img)
	source = '/static/images/'+file.filename
	print (source)
	return render_template("upload.html",faces=faces, AK=AK, NM=NM, source=source)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
