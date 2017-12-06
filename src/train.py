import h5py
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator

#Change directory to ../ak/train if reqd
train_ = '../nm/train'
cv_ = '../nm/validation'

epochs = 100
batch_size = 4

#To evaluate steps per epoch
train_samples = 600
imgw, imgh = 150, 150
cv_samples = 80

#Convert to std-img-format
if K.image_data_format() == 'channels_first':
    input_shape = (3, imgw, imgh)
else:
    input_shape = (imgw, imgh, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

#Image Generator used to make the model more robust
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2)

# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)
train_generator = train_datagen.flow_from_directory(
    train_,
    target_size=(imgw, imgh),
    batch_size=batch_size,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    cv_,
    target_size=(imgw, imgh),
    batch_size=batch_size,
    class_mode='binary')

model.fit_generator(
    train_generator,
    steps_per_epoch=train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=cv_samples // batch_size)






