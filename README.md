# Woof Demo V1

## Install

#### For production
Would recomend using the tensorflow docker image for server. The [Tensorflow getting started guide](https://www.tensorflow.org/versions/r0.11/get_started/os_setup.html) shows how to use docker instead of pip


#### For testing
* For CPU based osx, use `export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.11.0rc0-py2-none-any.whl`, then `sudo pip install --upgrade $TF_BINARY_URL`
* to use command line demo on an image, run `python classify_demo`
* you can specify an image: -i `path/to/image.jpg`
* If using GPU, you can specify memory


#### Run Server
1. Install TensorFlow: check [here](https://www.tensorflow.org/versions/r0.11/get_started/os_setup.html) to see what version works (cpu / gpu / osx / linux / docker)

2. To get all the other python requirements run `pip install -r requirements.txt`

3. Run `python webapp.py` to start server, then visit `localhost:5000`


## Notes
* `api.py` returns a json of predictions
the classifier engine relies on tensorflow and a pretrained model inside the `model/` directory. These files will get updated when the model is retrained. Specifically, `retrained_graph.pb` (the training model) and `retrained_labels.txt` (only if labels are added or removed)


## Changelog
* v1 (10/2016): switched to TensorFlow, doesn't rely on vagrant, retrainable with custom labels with docker image, faster and more maintainable
* v0 (4/2016): used overfeat model which ran on a isolated vagrant box. Retraining is very difficult, the weights are > 1gb, there is no flexibility on the labels and it is slow
