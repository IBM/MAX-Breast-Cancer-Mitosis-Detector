import pytest
import pycurl
import io
import json


def test_response():

    # Test True

    c = pycurl.Curl()
    b = io.BytesIO()
    c.setopt(pycurl.URL, 'http://localhost:5000/model/predict')
    c.setopt(pycurl.HTTPHEADER, ['Accept:application/json', 'Content-Type: multipart/form-data'])
    c.setopt(pycurl.HTTPPOST, [('image', (pycurl.FORM_FILE, "assets/true.png"))])
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.perform()
    assert c.getinfo(pycurl.RESPONSE_CODE) == 200
    c.close()
    response = b.getvalue()
    response = json.loads(response)

    assert response['status'] == 'ok'
    assert response['predictions'][0]['probability'] > 0.5

    # Test False

    c = pycurl.Curl()
    b = io.BytesIO()
    c.setopt(pycurl.URL, 'http://localhost:5000/model/predict')
    c.setopt(pycurl.HTTPHEADER, ['Accept:application/json', 'Content-Type: multipart/form-data'])
    c.setopt(pycurl.HTTPPOST, [('image', (pycurl.FORM_FILE, "assets/false.png"))])
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.perform()
    assert c.getinfo(pycurl.RESPONSE_CODE) == 200
    c.close()
    response = b.getvalue()
    response = json.loads(response)

    assert response['status'] == 'ok'
    assert response['predictions'][0]['probability'] < 0.5


if __name__ == '__main__':
    pytest.main([__file__])