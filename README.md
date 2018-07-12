# IBM Code Model Asset Exchange: Breast Cancer Mitosis Detector

The [Tumor Proliferation Assessment Challenge 2016 (TUPAC16)](http://tupac.tue-image.nl/) was created to develop state-of-the-art algorithms for automatic prediction of tumor proliferation scores from whole-slide histopathology images of breast tumors. The [IBM CODAIT](http://codait.org) team trained a mitosis detection model (a modified ResNet-50 model) on the [TUPAC16 auxiliary mitosis dataset](http://tupac.tue-image.nl/node/3), and then applied it to the whole slide images for predicting the tumor proliferation scores.

This repository contains code to instantiate and deploy the mitosis detection model mentioned above. This model takes a 64 x 64 PNG image file extracted from the whole slide image as input, and outputs the predicted probability of the image containing mitosis. For more information and additional features, check out the [deep-histopath](https://github.com/CODAIT/deep-histopath) repository on GitHub.

The code in this repository deploys the model as a web service in a Docker container. This repository was developed as part of the [IBM Code Model Asset Exchange](https://developer.ibm.com/code/exchanges/models/).

## Model Metadata
| Domain | Application | Industry  | Framework | Training Data | Input Data Format |
| ------------- | --------  | -------- | --------- | --------- | -------------- | 
| Vision | Cancer Classification | Health care | Keras | [TUPAC16](http://tupac.tue-image.nl/node/5) | 64x64 PNG Image|

_Note:_ Although this model supports different input data formats, the inference results are sensitive to the input data. In order to keep the extracted images the same as the original datasets, PNG image format should be used.


## References
* _Dusenberry, Mike, and Hu, Fei_, [Deep Learning for Breast Cancer Mitosis Detection](https://github.com/CODAIT/deep-histopath/raw/master/docs/tupac16-paper/paper.pdf), 2018.

## Licenses

| Component | License | Link  |
| ------------- | --------  | -------- |
| This repository | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [LICENSE](LICENSE) |
| Training Data | Custom License | [TUPAC16](http://tupac.tue-image.nl/node/5) |

## Pre-requisites:

* `docker`: The [Docker](https://www.docker.com/) command-line interface. Follow the
[installation instructions](https://docs.docker.com/install/) for your system.
* The minimum recommended resources for this model is 2GB Memory and 2 CPUs.

## Steps

1. [Build the Model](#1-build-the-model)
2. [Deploy the Model](#2-deploy-the-model)
3. [Use the Model](#3-use-the-model)
4. [Development](#4-development)
5. [Clean Up](#5-clean-up)

## 1. Build the Model

Clone the `MAX-Breast-Cancer-Mitosis-Detector` repository locally. In a terminal, run the following command:

```
$ git clone https://github.com/IBM/MAX-Breast-Cancer-Mitosis-Detector.git
```

Change directory into the repository base folder:

```
$ cd MAX-Breast-Cancer-Mitosis-Detector
```

To build the docker image locally, run: 

```
$ docker build -t max-breast-cancer-mitosis-detector .
```

All required model assets will be downloaded during the build process. _Note_ that currently this docker image is CPU
only (we will add support for GPU images later).

## 2. Deploy the Model

To run the docker image, which automatically starts the model serving API, run:

```
$ docker run -it -p 5000:5000 max-breast-cancer-mitosis-detector
```

## 3. Use the Model

The API server automatically generates an interactive Swagger documentation page. Go to `http://localhost:5000` to load
it. From there you can explore the API and also create test requests.

Use the `model/predict` endpoint to load a test image (you can use one of the test images from the `assets` folder) and
get predicted labels for the image from the API.

![Swagger Doc Screenshot](docs/swagger-screenshot.png)

You can also test it on the command line, for example:

```bash
$ curl -F "image=@assets/true.png" -XPOST http://127.0.0.1:5000/model/predict
```

You should see a JSON response like that below:

```json
{"predictions": [{"probability": 0.9884441494941711}], "status": "ok"}
```

## 4. Development

To run the Flask API app in debug mode, edit `config.py` to set `DEBUG = True` under the application settings. You will
then need to rebuild the docker image (see [step 1](#1-build-the-model)).

## 5. Cleanup

To stop the docker container type `CTRL` + `C` in your terminal.
