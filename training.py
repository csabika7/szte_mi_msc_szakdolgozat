import keras
from keras.models import Sequential
from keras.layers import Dense
# from keras.datasets import mnist
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
# from keras.utils import np_utils
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


# TODO Load data
# (X_train, y_train), (X_test, y_test) = mnist.load_data()
# X_train = X_train.reshape((X_train.shape[0], 28, 28, 1)).astype('float32')
# X_test = X_test.reshape((X_test.shape[0], 28, 28, 1)).astype('float32')
# X_train = X_train / 255
# X_test = X_test / 255
# y_train = np_utils.to_categorical(y_train)
# y_test = np_utils.to_categorical(y_test)

# Define model
model = define_model()

# TODO Train model
# model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5, batch_size=150)
# scores = model.evaluate(X_test, y_test, verbose=0)
# print("CNN Error: %.2f%%" % (100-scores[1]*100))

# Save model
model.save('./weed_model.hdf5')





def define_model():
    # dummy model for image testing
    m = Sequential()
    m.add(Conv2D(32, (5, 5), input_shape=(28, 28, 1), activation='relu'))
    m.add(MaxPooling2D())
    m.add(Flatten())
    m.add(Dense(128, activation='relu'))
    m.add(Dense(num_of_classes, activation='softmax'))
    # Compile model
    m.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return m