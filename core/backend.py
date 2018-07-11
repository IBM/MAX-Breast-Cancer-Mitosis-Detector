from PIL import Image
import io
import numpy as np
import logging
from config import DEFAULT_MODEL_PATH
import tensorflow
from train_mitoses import normalize

logger = logging.getLogger()


def read_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    if image.size != (64, 64):
        raise ValueError("The input file must be a PNG image of size (64, 64). Got %s %s." % (image.format, image.size))
    image = np.array(image)
    return image


def preprocess_image(image):
    image = np.expand_dims(image, 0)
    return image


def post_process_result(preds):
    return preds[0][0]


class ModelWrapper(object):
    """Model wrapper for Keras models"""
    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading model from: {}...'.format(path))
        self.sess = tensorflow.keras.backend.get_session()
        base_model = tensorflow.keras.models.load_model(path, compile=False)
        probs = tensorflow.keras.layers.Activation('sigmoid', name="sigmoid")(base_model.output)
        self.model = tensorflow.keras.models.Model(inputs=base_model.input, outputs=probs)
        self.input_tensor = self.model.input
        self.output_tensor = self.model.output

    def predict(self, x):
        x = preprocess_image(x)
        norm_patch_batch = normalize((np.array(x) / 255).astype(np.float32), "resnet_custom")
        out_batch = self.output_tensor.eval(feed_dict={self.input_tensor: norm_patch_batch}, session=self.sess)
        return post_process_result(out_batch)