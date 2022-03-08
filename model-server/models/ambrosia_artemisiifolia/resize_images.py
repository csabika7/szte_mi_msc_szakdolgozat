from scipy.ndimage import interpolation
import imageio as iio
from pathlib import Path
import os

TARGET_HEIGHT = 227
TARGET_WIDTH = 227

positive_samples_src_path = os.path.join(os.getcwd(), "training_db", "raw", "positive", "ratio_changed")
positive_samples_target_path = os.path.join(os.getcwd(), "training_db", "raw", "positive", "resized")
negative_samples_src_path = os.path.join(os.getcwd(), "training_db", "raw", "negative", "ratio_changed")
negative_samples_target_path = os.path.join(os.getcwd(), "training_db", "raw", "negative", "resized")


def read_image(path):
    return iio.imread(path, format="png")


def resize_image(image):
    zoom_x = TARGET_HEIGHT / image.shape[0]
    zoom_y = TARGET_WIDTH / image.shape[1]
    resized_image = interpolation.zoom(input=image, zoom=(zoom_x, zoom_y, 1))
    new_size = resized_image.shape
    if new_size[0] != TARGET_HEIGHT or new_size[1] != TARGET_WIDTH:
        raise RuntimeError("Invalid target image size height: {}, width: {}".format(*new_size))
    return resized_image


def write_image(image, path):
    iio.imwrite(uri=path, im=image, format="png")


def resize_all_images(input_dir, output_dir):
    for file in Path(input_dir).iterdir():
        original_image = read_image(file)
        resized_image = resize_image(original_image)
        write_image(resized_image, Path(output_dir, file.name))
    print("Resized all images from {} to {}", input_dir, output_dir)


resize_all_images(positive_samples_src_path, positive_samples_target_path)
resize_all_images(negative_samples_src_path, negative_samples_target_path)
