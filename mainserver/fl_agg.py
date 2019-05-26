from __future__ import print_function

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

import numpy as np
import glob

# batch_size = 128
num_classes = 10
# epochs = 1

# input image dimensions
img_rows, img_cols = 28, 28
input_shape = (img_rows, img_cols, 1)

def process_data():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    print(x_test.shape[0], 'test samples')

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    return x_train, x_test, y_train, y_test

def load_models():
    arr = []
    models = glob.glob("client_models/*.npy")
    for i in models:
        arr.append(np.load(i))

    return np.array(arr)

def fl_average():
    # FL average
    arr = load_models()
    fl_avg = np.average(arr, axis=0)

    for i in fl_avg:
        print(i.shape)

    return fl_avg


def build_model(avg):
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    model.set_weights(avg)

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    return model
    # model.fit(x_train, y_train,
    #           batch_size=batch_size,
    #           epochs=epochs,
    #           verbose=1,
    #           validation_data=(x_test, y_test))


def evaluate_model(model, x_test, y_test):
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

def save_agg_model(model):
    model.save("persistent_storage/agg_model.h5")
    print("Model written to storage!")

def model_aggregation():
    _, x_test, _, y_test =  process_data()
    avg = fl_average()
    model = build_model(avg)
    evaluate_model(model, x_test, y_test)
    save_agg_model(model)













