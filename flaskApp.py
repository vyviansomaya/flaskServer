from flask import Flask, render_template, request,redirect
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import requests

app = Flask(__name__)

app.config["FILE_UPLOAD_URL"] = 'https://patw1h5276.execute-api.eu-west-1.amazonaws.com/beta/upload'
app.config["ALLOWED_EXTENSIONS"] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_FILESIZE'] = 1 * 1024 * 1024

def allowed_file(filename):

	if not "." in filename:
		return False

	ext = filename.rsplit(".",1)[1]

	if ext in app.config["ALLOWED_EXTENSIONS"]:
		return True
	else:
		return False

def allowed_filesize(filesize):

	if int(filesize) <= app.config["MAX_FILESIZE"]:
	    return True
	else:
		return False

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/uploader', methods = ['Get', 'POST'])
def uploadFile():
	result=""
	if request.method == 'POST':

		if request.files:
			if not allowed_filesize(request.cookies.get("filesize")):
				result = "Files exceeded max size of 1 MB"
			else:
				uploadFile = request.files['file']
				uploadFile.save(secure_filename(uploadFile.filename))
        
				if not allowed_file(uploadFile.filename):
					result = "This file extention is not allowed"
				else:			
					response = requests.post(app.config["FILE_UPLOAD_URL"],files=uploadFile)
					if int(response.status_code)!=200:
						result = "File upload failed " + response.text
					else:
						result = "File upload successfull"

	return render_template("uploadFile.html",result = result)

if __name__ == '__main__':
	app.run(debug = True)
