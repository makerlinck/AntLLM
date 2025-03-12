import os

import tensorflow as tf
# tf.debugging.set_log_device_placement(True)
# tf.config.experimental.set_memory_growth(gpu[0], True)
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
# Create some tensors
a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
c = tf.matmul(a, b)


if __name__ == "__main__":
    # with tf.device("/gpu:0"):
    #     tf.random.set_seed(0)
    #     a = tf.random.uniform((10000, 10000), minval=0, maxval=3.0)
    #     c = tf.matmul(a, tf.transpose(a))
    #     d = tf.reduce_sum(c)
    import tensorflow as tf

    gpus = tf.config.list_physical_devices('GPU')
    print("is_built_with_cuda:", tf.test.is_built_with_cuda())
    print("Num GPUs Available: ", len(gpus))
    if gpus:
        for gpu in gpus:
            print("Name:", gpu.name, "Type:", gpu.device_type)