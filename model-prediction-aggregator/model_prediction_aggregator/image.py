from scipy.ndimage import interpolation
from numpy import asarray
from PIL import Image
import io


def resize_img(raw_img, width, height):
    img = asarray(Image.open(io.BytesIO(raw_img)))
    zoom_x = width / img.shape[0]
    zoom_y = height / img.shape[1]
    resized_image = interpolation.zoom(input=img, zoom=(zoom_x, zoom_y, 1))
    resized_img_bytes = io.BytesIO()
    Image.fromarray(resized_image).save(resized_img_bytes, format="png")
    return resized_img_bytes.getvalue()
