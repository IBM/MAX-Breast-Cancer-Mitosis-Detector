FROM codait/max-base:v1.1.0

RUN apt-get update && apt-get install -y libopenslide0 gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

RUN cd /workspace && \
    git clone https://github.com/codait/deep-histopath && \
    cp -R deep-histopath/. .

COPY . /workspace

EXPOSE 5000

CMD python /workspace/app.py
