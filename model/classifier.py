import tensorflow as tf
import sys


def classify(image_path, label_file, graph):
    #  Read image then load trained model graph
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()  #
    with tf.gfile.FastGFile(graph, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line in tf.gfile.GFile(label_file)]

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top = predictions[0].argsort()[-len(predictions[0]):][::-1]
        prediction = []
        for node_id in top:
            label = label_lines[node_id]
            score = predictions[0][node_id]
            prediction.append((label, score))  # tuple

        return prediction


if __name__ == '__main__':
    # run `python classifier.py path_to_image_file.jpg`

    # Classify image
    label_file = 'model/retrained_labels.txt'
    model_file = 'model/retrained_graph.pb'
    prediction = classify(sys.argv[1], label_file, model_file)
    for entry in prediction:
        label, score = entry
        print '%s\n  score = %f' % (label, score)

    print '\033[1;32m\nClassification: %s\nConfidence: %0.2f%%\n\033[1;m' % \
        (prediction[0][0], 100*prediction[0][1])
