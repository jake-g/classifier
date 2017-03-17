
echo 'Building backend...'
cp -r /app/label_image_backend /tensorflow/tensorflow/examples/label_image_backend
bazel build tensorflow/examples/label_image_backend:label_image_backend
bazel-bin/tensorflow/tensorflow/examples/label_image_backend/label_image_backend \
--output_layer=final_result \
--labels=/dogs/model/retrained_labels.txt \
--image=/dogs/model/test.jpg \
--graph=/dogs/model/retrained_graph.pb

echo 'Starting server...'
python /app/webapp.py
