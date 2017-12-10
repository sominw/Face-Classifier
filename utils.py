import time
import os

import cv2
from keras.models import load_model
import h5py
import numpy as np
from keras.preprocessing import image


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def detect_faces(f_cascade, colored_img, scaleFactor = 1.1):
    img_copy = colored_img.copy()
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    #haar_face_cascade = cv2.CascadeClassifier(os.path.join(APP_ROOT,'models/data/haarcascade_frontalface_alt.xml'))
    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5)
    print (len(faces))
    for (x, y, w, h) in faces:
        cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return len(faces), img_copy

def compile_models():
	model_nm = load_model(os.path.join(APP_ROOT,"models/nm_cnn.h5"))
	model_ak = load_model(os.path.join(APP_ROOT,"models/ak_cnn.h5"))
	model_nm.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
	model_ak.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

	return model_ak, model_nm

def check_ak_or_namo(path, model):
	img = image.load_img(path, target_size=(150,150))
	x = image.img_to_array(img)
	x = np.expand_dims(x, axis=0)
	images = np.vstack([x])
	classes = model.predict_classes(images, batch_size=10, verbose=0)
	if (classes[0][0]) == 1:
		return True
	else:
		return False