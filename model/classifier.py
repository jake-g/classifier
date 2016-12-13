import tensorflow as tf

N_PRED = 5  # default


def classify(image_path, label_file, graph, gpu_ratio=None):
    # GPU optional config
    # https://www.tensorflow.org/versions/r0.12/how_tos/using_gpu/index.html
    gpu_options = tf.GPUOptions(allow_growth = True)  # Default: only use necessary gpu memory
    if gpu_ratio:
        print('Using %d%% of GPU' % (100*gpu_ratio))
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_ratio)

    #  Read image then load trained model graph
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()  #
    with tf.gfile.FastGFile(graph, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line in tf.gfile.GFile(label_file)]

    # Predict
    sess_config = tf.ConfigProto(gpu_options=gpu_options)
    with tf.Session(config=sess_config) as sess:
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


def print_results(prediction):
    class colors:
        red = '\033[1;31m'
        green = '\033[1;32m'
        yellow = '\033[1;33m'
        stop = '\033[0m'  # stop color effect

    print ''
    for i, entry in enumerate(prediction[0:N_PRED]):
        label, score = entry
        if score > 0.6:
            color = colors.green
        elif score > 0.2:
            color = colors.yellow
        else:
            color = colors.red
        print color + '%d: %s (%0.1f%%)' % (i+1, label, 100 * score) + colors.stop

if __name__ == "__main__":
    LABELS = 'model/retrained_labels.txt'
    MODEL = 'model/retrained_graph.pb'

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", "-i", default="model/test.jpg", type=str, help="Image to classify")
    parser.add_argument("--model", "-m", default=MODEL, type=str, help="Frozen model file to import")
    parser.add_argument("--labels", "-l", default=LABELS, type=str, help="Frozen model file to import")
    parser.add_argument("--gpu", type=float, help="ratio of GPU memory per process (ex: 0.5)")
    args = parser.parse_args()


    # Classify image
    prediction = classify(args.image, args.labels, args.model, args.gpu)
    print_results(prediction)
