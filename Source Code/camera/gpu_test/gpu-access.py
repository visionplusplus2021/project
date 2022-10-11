import tensorflow as tf
from tensorflow.python.client import device_lib


physical_devices = tf.config.experimental.list_physical_devices('GPU')
print('Physical device list: ', physical_devices)
print("Local device list: ", device_lib.list_local_devices())
print("Config GPUs Available: ",tf.config.list_physical_devices('GPU'))

# if len(physical_devices) > 0:
#     tf.config.experimental.set_memory_growth(physical_devices[0], True)