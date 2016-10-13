import os

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask import Markup
from werkzeug import secure_filename

from model.classifier import classify

# Set up app
PORT = "5000"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg'}

# Set up classifier
n_predictions = 6
LABEL = 'model/retrained_labels.txt'
MODEL = 'model/retrained_graph.pb'


# Check filetype
def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# Classify image, return string
def run_classify(f):
    img_path = os.path.join('uploads', f)
    prediction = classify(img_path, LABEL, MODEL)
    try:  # Format output
        rank = []  # list holding results
        for entry in prediction[0:n_predictions]:
            label, score = entry
            rank.append('%.2f%% : %s' % (100 * score, label))
        return rank

    except ValueError:
        print 'ERROR'
        return None


# Home
@app.route('/')
def index():
    return render_template('index.html')


# Process Upload
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)  # remove unsupported chars
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(img_path)  # move image to upload folder
        return redirect(url_for('uploaded_file', filename=filename))


# Display Image
@app.route('/show/<filename>')
def uploaded_file(filename):
    data = ''
    endpoint = 'http://127.0.0.1:5000/uploads/' + filename
    result = run_classify(filename)

    for line in result:
        print line
        data += Markup('<li>%s</li>' % line)
    print '\n'
    return render_template('result.html', filename=endpoint, data=data)


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Default
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(PORT), debug=True)
