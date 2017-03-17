#!/bin/bash
export TF_CPP_MIN_LOG_LEVEL=2  # turn off warnings

echo 'Building backend...'
cd /tensorflow
cp -r /app/model/label_image_backend tensorflow/examples/label_image_backend
bazel build tensorflow/examples/label_image_backend:label_image_backend

echo 'Starting server...'
cd /app
pip install -r requirements.txt
python webapp.py
