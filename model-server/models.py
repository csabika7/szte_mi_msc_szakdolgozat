import tensorflow as tf

print('Loading model...')
weed_model = tf.keras.models.load_model('/root/weed_model.hdf5')
print('Model loaded')
