import os
import time

from flask import Flask, render_template, request
from werkzeug import secure_filename
import cv2
import numpy as np

from utils import detect_faces, compile_models, check_ak_or_namo

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

model_ak, model_nm = compile_models()
haar_face_cascade = cv2.CascadeClassifier(os.path.join(APP_ROOT,'models/data/haarcascade_frontalface_alt.xml'))

@app.route("/")
def index():
	return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
	target = os.path.join(APP_ROOT, 'static/images/')
	print (target)

	if not os.path.isdir(target):
		os.mkdir(target)

	file = request.files['file']
	print (file)
	filename = file.filename
	destination = 'static/images/'+str(secure_filename(file.filename))
	file.save(destination)
	time.sleep(2)
	print ("Location:" + destination)
	img = cv2.imread(destination)
	n_faces, faces_detected_img = detect_faces(haar_face_cascade, img)
	faces="No"
	AK="No"
	NM="No"
	if n_faces > 0:
		faces = "Yes"
		if (check_ak_or_namo(destination, model_ak) == True):
			AK = "Yes"
		if (check_ak_or_namo(destination, model_nm) == True):
			NM = "Yes"
	cv2.imwrite(destination, faces_detected_img)
	source = '/static/images/'+file.filename
	print (source)
	return render_template("upload.html",faces=faces, AK=AK, NM=NM, source=source)

