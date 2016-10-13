# Woof Demo V2

## Install

Install TensorFlow: check [here](https://www.tensorflow.org/versions/r0.11/get_started/os_setup.html) to see what version works (cpu / gpu / osx / linux) (use the pip method)

For CPU based osx, use `export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.11.0rc0-py2-none-any.whl`, then `sudo pip install --upgrade $TF_BINARY_URL`

to get all the other python requirements run `pip install -r requirements.txt`

run `python app.py` to start server, then visit `localhost:5000`

to use command line demo on an image, run `python classify_demo
path/to/image.jpg`


## Notes

the classifier engine relies on tensorflow and a pretrained model inside the `model/` directory


## Changelog
* v1 (10/2016): switched to TensorFlow, doesn't rely on vagrant, retrainable with custom labels with docker image, faster and more maintainable
* v0 (4/2016): used overfeat model which ran on a isolated vagrant box. Retraining is very difficult, the weights are > 1gb, there is no flexibility on the labels and it is slow