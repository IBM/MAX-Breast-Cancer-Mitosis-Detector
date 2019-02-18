# Application settings

# Flask settings 
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# API metadata
API_TITLE = 'MAX Breast Cancer Mitosis Detector'
API_DESC = 'Predict the probability of the input image containing mitosis.'
API_VERSION = '0.1'

# default model
MODEL_NAME = 'MAX Breast Cancer Mitosis Detector'
DEFAULT_MODEL_PATH = 'assets/deep_histopath_model.hdf5'

MODEL_LICENSE = "Custom"  # TODO - what are we going to release this as?

MODEL_META_DATA = {
    'id': '{}'.format(MODEL_NAME.lower()),
    'name': '{} Keras Model'.format(MODEL_NAME),
    'description': '{} Keras model trained on TUPAC16 data to detect mitosis'.format(MODEL_NAME),
    'type': 'image_classification',
    'license': '{}'.format(MODEL_LICENSE)
}
