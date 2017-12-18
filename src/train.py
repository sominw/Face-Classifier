import h5py #save model
import pickle as pk
import argparse
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.optimizers import Adam
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

parser = argparse.ArgumentParser()
parser.add_argument('-epochs', type=int, default=25)
parser.add_argument('-batch_size', type=int, default=64)
args = parser.parse_args()

#Change directory to ../<reqd>/train if reqd
train_ = '../nm/train'
cv_ = '../nm/validation'

epochs = args.epochs
batch_size = args.batch_size

#To evaluate steps per epoch
train_samples = 1000
imgw, imgh = 150, 150
cv_samples = 400

#Conversion to I/P Format
if K.image_data_format() == 'channels_first':
    input_shape = (3, imgw, imgh)
else:
    input_shape = (imgw, imgh, 3)

model = Sequential()

model.add(Conv2D(64, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
"""
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
"""
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

#model.add(Conv2D(64, (3, 3)))
#model.add(Activation('relu'))
#model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(32))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

adam = Adam(lr=0.001)

model.compile(loss='binary_crossentropy',
              optimizer=adam,
              metrics=['accuracy'])

#Image Generator used to make the model more robust
train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, horizontal_flip=True, zoom_range=0.2)

# rescale only
test_datagen = ImageDataGenerator(rescale=1. / 255)
train_generator = train_datagen.flow_from_directory(train_, target_size=(imgw, imgh), batch_size=batch_size, class_mode='binary')
validation_generator = test_datagen.flow_from_directory(cv_, target_size=(imgw, imgh), batch_size=batch_size, class_mode='binary')

history = model.fit_generator(train_generator, steps_per_epoch=train_samples // batch_size, epochs=epochs, validation_data=validation_generator,
    validation_steps=cv_samples // batch_size)

""" filepath = "weight-improv-{epoch:02d}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='accuracy', verbose=1, save_best_only=True, mode = 'max')
callbacks_list=[checkpoint] """

#tensorboard = TensorBoard(log_dir='/output/Graph', histogram_freq=0, write_graph=True, write_images=True)

#Change path for nm/ak
model.save('../models/nm_cnn.h5')
#pk.dump(history.history, open("model_history_nm.sav","wb"))


