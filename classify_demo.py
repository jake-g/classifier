import sys
from model.classifier import classify

# Init
label_file = 'model/retrained_labels.txt'
model_file = 'model/retrained_graph.pb'

# Classify image
prediction = classify(sys.argv[1], label_file, model_file)

# Print Results (#1 in green first)
top = prediction[0]
print '\033[1;32m\n%s (%0.1f%%)\033[1;m' % (top[0], 100 * top[1])
for entry in prediction[1:5]:
    label, score = entry
    print '%s (%0.1f%%)' % (label, 100 * score)
