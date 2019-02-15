from core.model import ModelWrapper
from flask_restplus import fields, abort
from werkzeug.datastructures import FileStorage
from maxfw.core import MAX_API, PredictAPI

input_parser = MAX_API.parser()
input_parser.add_argument('image', type=FileStorage, location='files', required=True,
                          help='An image file encoded as PNG with the size 64*64')

label_prediction = MAX_API.model('LabelPrediction', {
    'probability': fields.Float(required=True, description='Probability of the image containing mitosis')
})

predict_response = MAX_API.model('ModelPredictResponse', {
    'status': fields.String(required=True, description='Response status message'),
    'predictions': fields.List(fields.Nested(label_prediction), description='Predicted labels and probabilities')
})


class ModelPredictAPI(PredictAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc('predict')
    @MAX_API.expect(input_parser)
    @MAX_API.marshal_with(predict_response)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}

        args = input_parser.parse_args()

        try:
            image_data = args['image'].read()
            image = self.model_wrapper._read_image(image_data)
            preds = self.model_wrapper.predict(image)
            label_preds = [{'probability': float(preds)}]
            result['predictions'] = label_preds
            result['status'] = 'ok'
        except ValueError as e:
            abort(400, str(e))

        return result