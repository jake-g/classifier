# Woof Demo V2


## Build Docker Image
`docker build -t puppy-server .`

## Run Container
docker run -it -p 5000:5000 -v /Users/jake/Dropbox/projects/puppyai/webapp/:/app/ tensorflow/tensorflow:nightly-devel

## Notes
the classifier engine relies on tensorflow and a pretrained model inside the `model/` directory. These files will get updated when the model is retrained. Specifically, `retrained_graph.pb` (the training model) and `retrained_labels.txt` (only if labels are added or removed)


## Changelog
* v2 (3/2017): Docker container for everything. Uses c++ backend for faster predictions
* v1 (10/2016): switched to TensorFlow, doesn't rely on vagrant, retrainable with custom labels with docker image, faster and more maintainable
* v0 (4/2016): used overfeat model which ran on a isolated vagrant box. Retraining is very difficult, the weights are > 1gb, there is no flexibility on the labels and it is slow
