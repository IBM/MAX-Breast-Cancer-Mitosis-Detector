import pytest
import requests


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'MAX Breast Cancer Mitosis Detector'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'max breast cancer mitosis detector-keras-model'
    assert metadata['name'] == 'MAX Breast Cancer Mitosis Detector Keras Model'
    assert metadata['description'] == 'MAX Breast Cancer Mitosis Detector Keras model trained on TUPAC16 data to detect mitosis'
    assert metadata['license'] == 'Custom'


def test_predict():
    model_endpoint = 'http://localhost:5000/model/predict'
    true_path = 'assets/true.png'
    false_path = 'assets/false.png'

    # Test True

    with open(true_path, 'rb') as file:
        file_form = {'image': (true_path, file, 'image/png')}
        r = requests.post(url=model_endpoint, files=file_form)
    assert r.status_code == 200

    response = r.json()

    assert response['status'] == 'ok'
    assert response['predictions'][0]['probability'] > 0.5

    # Test False

    with open(false_path, 'rb') as file:
        file_form = {'image': (false_path, file, 'image/png')}
        r = requests.post(url=model_endpoint, files=file_form)
    assert r.status_code == 200

    response = r.json()

    assert response['status'] == 'ok'
    assert response['predictions'][0]['probability'] < 0.5


if __name__ == '__main__':
    pytest.main([__file__])
