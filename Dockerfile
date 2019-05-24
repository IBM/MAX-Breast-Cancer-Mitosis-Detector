FROM codait/max-base:v1.1.1

ARG model_bucket=http://max-assets.s3.us.cloud-object-storage.appdomain.cloud/max-breast-cancer-mitosis-detector/v1.0
ARG model_file=assets.tar.gz

RUN apt-get update && apt-get install -y libopenslide0 gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=assets/${model_file} && \
  tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

RUN cd /workspace && \
    git clone https://github.com/codait/deep-histopath && \
    cd deep-histopath && \
    cd ../ && \
    cp -R deep-histopath/. .

COPY . /workspace

RUN md5sum -c md5sums.txt # check file integrity

EXPOSE 5000

CMD python /workspace/app.py
