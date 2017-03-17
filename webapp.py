import os
import argparse

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask import Markup
from werkzeug import secure_filename

from model.classifier import classify, print_top_n

# SETTINGS
N_PREDS = 5
LABELS = 'model/retrained_labels.txt'
MODEL = 'model/retrained_graph.pb'
PORT = 5000

# Set up app
app = Flask(__name__)
# cors = CORS(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get('PORT', PORT))
app.config['LABELS'] = os.path.join(APP_ROOT, LABELS)
app.config['MODEL'] = os.path.join(APP_ROOT, MODEL)
app.config['UPLOAD_FOLDER'] = os.path.join(APP_ROOT, 'uploads/')
app.config['ALLOWED_EXTENSIONS'] = {'bmp', 'png', 'jpg', 'jpeg'}


# Check filetype
def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# Classify image, return string
def run_classify(f):
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], f)
    print('starting classifier...')
    results = classify(img_path, args.labels, args.model)
    print_top_n(results, n=N_PREDS)
    try:  # Format output
        rank = []  # list holding results
        for i in range(N_PREDS):
            pos = str(i)  # position key from best (0) to worst (n)
            label = str(results[pos]['breed'])
            score = float(results[pos]['score'])
            rank.append('%.2f%% : %s' % (100 * score, label))
        return rank
    except:
        print('Classification failed')
        return None


# Home
@app.route('/')
def index():
    return render_template('index.html')


# Process Upload
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    print('starting processing uploaded file...')
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)  # remove unsupported chars
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            print('trying to save file... %s' % filename)
            f.save(img_path)  # move image to upload folder
            return redirect(url_for('uploaded_file', filename=filename))
        except:
            print('Could not move uploaded image')
            return None


# Display Image
@app.route('/show/<filename>')
def uploaded_file(filename):
    data = ''
    endpoint = 'http://127.0.0.1:' + str(PORT) + '/uploads/' + filename
    result = run_classify(filename)
    json = jsonify(tokens=result, imageurl=endpoint)

    for line in result:
        data += Markup('<li>%s</li>' % line)
    return render_template('result.html', filename=endpoint, data=data)


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Default
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", default=app.config['MODEL'], type=str, help="trained model")
    parser.add_argument("--labels", "-l", default=app.config['LABELS'], type=str, help="list of labels")
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=int(PORT), debug=True)
