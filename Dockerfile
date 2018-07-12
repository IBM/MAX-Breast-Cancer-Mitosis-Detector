FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y libopenslide0 gcc && rm -rf /var/lib/apt/lists/*

# Python package versions
ARG numpy_version=1.14.1
ARG tensorflow_version=1.9.0

RUN pip install --upgrade pip && \
    pip install numpy==${numpy_version} && \
    pip install Pillow && \
    pip install h5py && \
    pip install flask-restplus && \
    pip install openslide-python && \
    pip install tensorflow==${tensorflow_version}

RUN mkdir /workspace && \
    cd /workspace && \
    git clone https://github.com/codait/deep-histopath && \
    cp -R deep-histopath/. .

COPY . /workspace

EXPOSE 5000

CMD python /workspace/app.py
