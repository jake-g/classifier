# Woof Demo V2

#### Run Server
1. Install TensorFlow: check [here](https://www.tensorflow.org/versions/r0.11/get_started/os_setup.html) to see what version works (cpu / gpu / osx / linux / docker)

2. To get all the other python requirements run `pip install -r requirements.txt`

3. Run `python webapp.py` to start server, then visit `localhost:5000`


## Notes
the classifier engine relies on tensorflow and a pretrained model inside the `model/` directory. These files will get updated when the model is retrained. Specifically, `retrained_graph.pb` (the training model) and `retrained_labels.txt` (only if labels are added or removed)


## Changelog
* v2 (3/2017): Docker container for everything. Uses c++ backend for faster predictions
* v1 (10/2016): switched to TensorFlow, doesn't rely on vagrant, retrainable with custom labels with docker image, faster and more maintainable
* v0 (4/2016): used overfeat model which ran on a isolated vagrant box. Retraining is very difficult, the weights are > 1gb, there is no flexibility on the labels and it is slow
