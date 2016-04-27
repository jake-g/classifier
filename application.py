import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import subprocess
from flask import Markup

# Set up app
PORT = "5000"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'bmp', 'png', 'jpg', 'jpeg', 'gif'}


# Check filetype
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# Classify image, return string
# TODO return json formate
def run_classify(f, n):
	img_path = os.path.join('uploads', f)
	overfeat = 'classifier/overfeat'
	p = subprocess.Popen([overfeat, '-n', str(n), img_path], stdout=subprocess.PIPE)
	(out, err) = p.communicate()
	try:  # Format output
		rank = []  # list holding results
		results = out.strip().split('\n')
		for i, result in enumerate(results):
			toks = result.split()
			if toks:
				p = float(toks[-1])
				return_str = ' '.join(toks[0:-1])
				rank.append('%.2f %% : %s' % (100 * p, return_str))
	except ValueError:
		print err
	return rank


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
	n_guesses = 6
	endpoint = 'http://127.0.0.1:5000/uploads/' + filename
	result = run_classify(filename, n_guesses)

	for line in result:
		print line
		data += Markup('<li>%s</li>' % line)
	return render_template('result.html', filename=endpoint, data=data)


@app.route('/uploads/<filename>')
def send_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Default
if __name__ == '__main__':
	app.run(
		host="0.0.0.0",
		port=int(PORT),
		debug=True
	)
