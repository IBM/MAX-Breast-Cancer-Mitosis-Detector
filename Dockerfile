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

FROM quay.io/codait/max-base:v1.4.0

ARG model_bucket=https://max-cdn.cdn.appdomain.cloud/max-breast-cancer-mitosis-detector/1.0.1
ARG model_file=assets.tar.gz

RUN sudo apt-get update && sudo apt-get install -y libopenslide0 gcc && sudo rm -rf /var/lib/apt/lists/*

RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=assets/${model_file} && \
  tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN git clone https://github.com/codait/deep-histopath && \
    cd deep-histopath && \
    git checkout c8baf8d47b6c08c0f6c7b1fb6d5dd6b77e711c33 && \
    cd - && \
    mv -n deep-histopath/* .

COPY . .

# check file integrity
RUN sha512sum -c sha512sums.txt

EXPOSE 5000

CMD python app.py
