from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

UPLOAD_FOLDER ='https://patw1h5276.execute-api.eu-west-1.amazonaws.com/beta/upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config["FILE_UPLOADS"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/contact')
def contact():
	return render_template("contact.html")

@app.route('/uploader', methods = ['Get', 'POST'])
def uploadFile():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		return ' File was uploaded successfully'
	return render_template("uploadFile.html")


if __name__ == '__main__':
	app.run(debug = True)