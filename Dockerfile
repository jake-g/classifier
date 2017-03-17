FROM tensorflow/tensorflow:nightly-devel

RUN mkdir -p /tmp
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR '/tensorflow'
COPY model/label_image_backend tensorflow/examples/label_image_backend
RUN bazel build tensorflow/examples/label_image_backend:label_image_backend

WORKDIR '/app'
ENV TF_CPP_MIN_LOG_LEVEL 2
ENTRYPOINT ['python']
CMD ['app.py']
