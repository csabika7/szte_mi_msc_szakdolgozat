import keras
import tensorflow as tf


class Model:

    def __init__(self, model_file_path: str):
        self.model = tf.keras.models.load_model(model_file_path)

    def predict(self, img_input: tf.Tensor):
        keras.Model
        return self.model.predict(img_input)


def convert_img_to_model_input(raw_img):
    img_tensor = tf.io.decode_image(raw_img, channels=3)
    img = tf.reshape(img_tensor, (1, 227, 227, 3))
    return img

