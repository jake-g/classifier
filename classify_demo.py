import argparse
from model.classifier import classify, print_results

LABELS = 'model/retrained_labels.txt'
MODEL = 'model/retrained_graph.pb'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", "-i", default="model/test.jpg", type=str, help="Image to classify")
    parser.add_argument("--model", "-m", default=MODEL, type=str, help="Frozen model file to import")
    parser.add_argument("--labels", "-l", default=LABELS, type=str, help="Frozen model file to import")
    parser.add_argument("--gpu", type=float, help="ratio of GPU memory per process (ex: 0.5)")
    args = parser.parse_args()


    # Classify image
    prediction = classify(args.image, args.labels, args.model, args.gpu)
    print_results(prediction)