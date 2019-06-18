#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from PIL import Image
import io
import numpy as np
import logging

import tensorflow
from maxfw.model import MAXModelWrapper

from config import DEFAULT_MODEL_PATH, MODEL_NAME
from train_mitoses import normalize

logger = logging.getLogger()


class ModelWrapper(MAXModelWrapper):

    MODEL_META_DATA = {
        'id': '{}-keras-model'.format(MODEL_NAME.lower()),
        'name': '{} Keras Model'.format(MODEL_NAME),
        'description': '{} Keras model trained on TUPAC16 data to detect mitosis'.format(MODEL_NAME),
        'type': 'image_classification',
        'license': 'Custom',
        'source': 'https://developer.ibm.com/exchanges/models/all/max-breast-cancer-mitosis-detector/'
    }

    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading model from: {}...'.format(path))
        self.sess = tensorflow.keras.backend.get_session()
        base_model = tensorflow.keras.models.load_model(path, compile=False)
        probs = tensorflow.keras.layers.Activation('sigmoid', name="sigmoid")(base_model.output)
        self.model = tensorflow.keras.models.Model(inputs=base_model.input, outputs=probs)
        self.input_tensor = self.model.input
        self.output_tensor = self.model.output

    def _read_image(self, image_data):
        image = Image.open(io.BytesIO(image_data))
        if image.size != (64, 64):
            raise ValueError(
                "The input file must be a PNG image of size (64, 64). Got %s %s." % (image.format, image.size))
        image = np.array(image)
        return image

    def _pre_process(self, image):
        image = np.expand_dims(image, 0)
        return image

    def _post_process(self, preds):
        return preds[0][0]

    def _predict(self, x):
        norm_patch_batch = normalize((np.array(x) / 255).astype(np.float32), "resnet_custom")
        out_batch = self.output_tensor.eval(feed_dict={self.input_tensor: norm_patch_batch}, session=self.sess)
        return out_batch
