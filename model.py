import tensorflow as tf

print('Loading model...')
model = tf.keras.models.load_model('/root/model.hdf5')

print('Model loaded')

# TODO do predict
# model.predict(data)