from pathlib import Path
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten, BatchNormalization, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg16 import VGG16
import os


# Define model
def alex_net():
    m = Sequential()
    m.add(Conv2D(filters=96, kernel_size=(11, 11), strides=(4, 4), activation='relu', input_shape=(227, 227, 1)))
    m.add(BatchNormalization())
    m.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
    m.add(Conv2D(filters=256, kernel_size=(5, 5), strides=(1, 1), activation='relu'))
    m.add(BatchNormalization())
    m.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
    m.add(Conv2D(filters=384, kernel_size=(3, 3), strides=(1, 1), activation='relu'))
    m.add(Conv2D(filters=384, kernel_size=(3, 3), strides=(1, 1), activation='relu'))
    m.add(Conv2D(filters=256, kernel_size=(3, 3), strides=(1, 1), activation='relu'))
    m.add(Flatten())
    m.add(Dense(4096, activation='relu'))
    m.add(Dropout(0.5))
    m.add(Dense(4096, activation='relu'))
    m.add(Dense(1, activation='sigmoid'))

    m.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return m


def vgg16():
    base_model = VGG16(
        include_top=False,
        weights="imagenet",
        input_tensor=None,
        input_shape=(227, 227, 3),
        pooling="max",
        classes=2
    )
    base_model.trainable = False

    m = Sequential([
        base_model,
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(512, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    m.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return m


# Load data

TRAINING_DIR = os.path.join(Path(os.getcwd()).parent.parent, "training_db", "preprocessed", "train")
VALIDATION_DIR = os.path.join(Path(os.getcwd()).parent.parent, "training_db", "preprocessed", "validation")
BATCH_SIZE = 8
generator = ImageDataGenerator()

train = generator.flow_from_directory(
    directory=TRAINING_DIR,
    target_size=(227, 227),
    class_mode="binary",
    batch_size=BATCH_SIZE
)

validation = generator.flow_from_directory(
    directory=VALIDATION_DIR,
    target_size=(227, 227),
    class_mode="binary",
    batch_size=BATCH_SIZE
)

# model = alex_net()
model = vgg16()

# training
model.fit(train, steps_per_epoch=451/BATCH_SIZE, epochs=10, validation_data=validation, validation_steps=112/BATCH_SIZE)
scores = model.evaluate(validation, verbose=0)

# evaluation
print("CNN Error: %.2f%%" % (100-scores[1]*100))

# Save model
model.save(os.path.join(os.getcwd(), "weed_model.hdf5"))
