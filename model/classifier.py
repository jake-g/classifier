import json
import subprocess

def classify(image_path, label_file, graph_file):
    cmd = '/tensorflow/bazel-bin/tensorflow/examples/label_image_backend/label_image_backend'
    classify_cmd = [
        cmd,
        '--output_layer=final_result',
        '--labels={labels}'.format(labels=label_file),
        '--image={img}'.format(img=image_path),
        '--graph={graph}'.format(graph=graph_file)
    ]
    res = subprocess.check_output(
        classify_cmd)  # json formatted str of results
    return json.loads(res)  # return json as object


def print_top_n(results, n=5):
    class colors:
        red = '\033[1;31m'
        green = '\033[1;32m'
        yellow = '\033[1;33m'
        stop = '\033[0m'  # stop color effect

    for i in range(n):
        pos = str(i)  # position key from best (0) to worst (n)
        try:
            label = str(results[pos]['breed'])
            score = float(results[pos]['score'])
        except:
            print 'Error parsing result %d\n%r' % (i, results[pos])
        if score > 0.6:
            color = colors.green
        elif score > 0.2:
            color = colors.yellow
        else:
            color = colors.red
        print color + '%d: %s (%0.1f%%)' \
                % (i + 1, label, 100 * score) + colors.stop


if __name__ == "__main__":
    LABELS = '/dogs/model/retrained_labels.txt'
    MODEL = '/dogs/model/retrained_graph.pb'
    IMG = '/dogs/model/test.jpg'

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        "-i",
        default=IMG,
        type=str,
        help="Image to classify")
    parser.add_argument(
        "--model",
        "-m",
        default=MODEL,
        type=str,
        help="Frozen model file to import")
    parser.add_argument(
        "--labels",
        "-l",
        default=LABELS,
        type=str,
        help="Frozen model file to import")
    args = parser.parse_args()

    # Classify image
    res = classify(args.image, args.labels, args.model)
    print_top_n(res, n=10)
